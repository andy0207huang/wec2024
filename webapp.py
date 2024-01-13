# ---WEBAPP---
import pandas as pd
import streamlit as st
import pydeck as pdk

from backend.dataHandle import getAllData, addRow, editData

## Set page configuration
st.set_page_config(
    page_title="WEC 2024 - Natural Disaster", page_icon=":bar_chart:", layout="centered"
)

## LOAD CSV
dfcsv = pd.read_csv("MOCK_DATA.csv")

## TITLE
st.title("🌎🌊🌀🌪️ Natural Disaster Webapp")
st.markdown("##")

## SIDEBAR FILTER
# Sidebar - Filter by Name
with st.sidebar.expander("Filter by Name:", expanded=True):
    disasterName = st.multiselect(
        "Select the Disaster Name:",
        options=dfcsv["Name"].unique(),
        default=dfcsv["Name"].unique(),
    )

# Sidebar - Filter by Type
with st.sidebar.expander("Filter by Type:", expanded=True):
    disasterType = st.multiselect(
        "Select the Disaster Type:",
        options=dfcsv["type"].unique(),
        default=dfcsv["type"].unique(),
    )

# Sidebar - Filter by Intensity
with st.sidebar.expander("Filter by Intensity:", expanded=False):
    selected_intensity = st.slider("Select Intensity Range:", 1, 10, (1, 10))

# Sidebar - Filter by Date
with st.sidebar.expander("Filter by Date:", expanded=False):
    start_date, end_date = st.select_slider(
        "Select Date Range:",
        options=dfcsv["date"].unique(),
        value=(dfcsv["date"].min(), dfcsv["date"].max()),
    )

# Collapsible section for adding new disaster entry
with st.expander("Add New Disaster Event", expanded=False):
    new_name = st.text_input("Name", "Hurricane X")
    new_longitude = st.number_input("Longitude", value=0.0)
    new_latitude = st.number_input("Latitude", value=0.0)
    new_date = st.date_input("Date")
    new_intensity = st.slider("Intensity", 1, 10, 5)
    new_type = st.selectbox(
        "Type", ["tornado", "hurricane", "earthquake", "flood", "wildfire"]
    )

    add_button = st.button("Add Disaster")
    if add_button:
        new_data = pd.DataFrame(
            [
                {
                    "Name": new_name,
                    "long": new_longitude,
                    "lat": new_latitude,
                    "date": new_date,
                    "intensity": new_intensity,
                    "type": new_type,
                }
            ]
        )
        # Append new data to dataframe
        dfcsv = pd.concat([dfcsv, new_data], ignore_index=True)
        # Update CSV file
        dfcsv.to_csv("MOCK_DATA.csv", index=False)
        st.success("Added New Disaster: " + new_name)

# Collapsible section for deleting an entry
with st.expander("Delete Disaster Event", expanded=False):
    delete_name = st.selectbox("Select the Name to Delete:", options=dfcsv["Name"].unique())
    if st.button("Delete"):
        dfcsv = dfcsv[dfcsv["Name"] != delete_name]
        dfcsv.to_csv("MOCK_DATA.csv", index=False)
        st.success("Deleted Disaster Sucessfully: " + new_name)

# Collapsible section for editing a disaster event
with st.expander("Edit Disaster Event", expanded=False):
    edit_name = st.selectbox("Select the Name to Edit:", options=dfcsv["Name"].unique())

    # Pre-fill information for name is selected
    disaster_info = dfcsv[dfcsv['Name'] == edit_name].iloc[0]

    new_name = st.text_input("New Name (leave blank to keep original)", value="")
    new_type = st.multiselect("Type", options=dfcsv["type"].unique(), default=disaster_info['type'])
    new_date = st.text_input("New Date", value=disaster_info['date'])
    intensity_options = list(range(1, 11))  # Creates a list of integers from 1 to 10
    new_intensity = st.multiselect("Intensity", options=intensity_options, default=[disaster_info['intensity']])
    new_longitude = st.text_input("New Longitude", value=disaster_info['long'])
    new_latitude = st.text_input("New Latitude", value=disaster_info['lat'])

    if st.button("Save Edits"):
        # Add code here to edit into csv file
        st.success("Disaster details updated.")

# Applying Filters
df_selection = dfcsv.query(
    "Name == @disasterName & type == @disasterType & intensity >= @selected_intensity[0] & intensity <= @selected_intensity[1] & date >= @start_date & date <= @end_date"
)

## MAP
# Map COLOUR by Type
disaster_color_map = {
    "tornado": [255, 255, 0, 180],  # yellow
    "hurricane": [169, 169, 169, 180],  # gray
    "flood": [0, 0, 255, 180],  # blue
    "earthquake": [165, 42, 42, 180],  # brown
}
df_selection["color"] = df_selection["type"].map(disaster_color_map)

# Map default
view_state = pdk.ViewState(
    latitude=df_selection["lat"].mean() if not df_selection.empty else 0,
    longitude=df_selection["long"].mean() if not df_selection.empty else 0,
    zoom=1,
    pitch=50,
)

# Map layer show plat based on csv
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_selection,
    get_position="[long, lat]",  # location
    get_radius="intensity * 50000",  # intensity difer by radius
    get_color="color",  # get from previous colour mapping
    pickable=True,
    auto_highlight=True,
)

render = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer],
    tooltip={
        "html": 
            "<b>Disaster Name: </b> {Name} <br /> "
            "<b>Longitude: </b> {long} <br /> "
            "<b>Latitude: </b>{lat} <br /> "
            "<b>Date: </b>{date} <br />"
            "<b>Intensity: </b>{intensity} <br />"
            "<b>Type: </b>{type} <br />"
    },
)
render


## RAW TABLE DATA
st.header("Filtered Data")
st.dataframe(df_selection)