# ---WEBAPP---
import pandas as pd
import streamlit as st
import pydeck as pdk

# Set page configuration
st.set_page_config(
    page_title="WEC 2024 - Natural Disaster",
    page_icon=":bar_chart:",
    layout="centered"
)

# Load data
dfcsv = pd.read_csv("MOCK_DATA.csv")

# Dashboard title
st.title(":bar_chart: Natural Disaster Webapp")
st.markdown("##")

# Sidebar - Filter by Name
with st.sidebar.expander("Filter by Name:", expanded=True):
    disasterName = st.multiselect(
        "Select the Disaster Name:",
        options=dfcsv["Name"].unique(),
        default=dfcsv["Name"].unique()
    )

# Sidebar - Filter by Type
with st.sidebar.expander("Filter by Type:", expanded=True):
    disasterType = st.multiselect(
        "Select the Disaster Type:",
        options=dfcsv["type"].unique(),
        default=dfcsv["type"].unique()
    )

# Sidebar - Filter by Intensity
with st.sidebar.expander("Filter by Intensity:", expanded=False):
    selected_intensity = st.slider("Select Intensity Range:", 1, 10, (1, 10))

# Sidebar - Filter by Date
with st.sidebar.expander("Filter by Date:", expanded=False):
    start_date, end_date = st.select_slider(
        "Select Date Range:",
        options=dfcsv["date"].unique(),
        value=(dfcsv["date"].min(), dfcsv["date"].max())
    )

# Collapsible section for adding new disaster entry
with st.expander("Add New Disaster Event", expanded=False):
    new_name = st.text_input("Name", "Hurricane X")
    new_longitude = st.number_input("Longitude", value=0.0)
    new_latitude = st.number_input("Latitude", value=0.0)
    new_date = st.date_input("Date")
    new_intensity = st.slider("Intensity", 1, 10, 5)
    new_type = st.selectbox("Type", ["tornado", "hurricane", "earthquake", "flood", "wildfire"])

    add_button = st.button("Add Disaster")
    if add_button:
        new_data = pd.DataFrame([{
            "Name": new_name,
            "long": new_longitude,
            "lat": new_latitude,
            "date": new_date,
            "intensity": new_intensity,
            "type": new_type
        }])
        # Append new data to dataframe
        dfcsv = pd.concat([dfcsv, new_data], ignore_index=True)
        # Update CSV file
        dfcsv.to_csv("MOCK_DATA.csv", index=False)
        st.success("Added New Disaster: " + new_name)

# Applying Filters
df_selection = dfcsv.query(
    "Name == @disasterName & type == @disasterType & intensity >= @selected_intensity[0] & intensity <= @selected_intensity[1] & date >= @start_date & date <= @end_date"
)

# Map Visualization
disaster_color_map = {
    'tornado': [255, 255, 0, 180],
    'hurricane': [169, 169, 169, 180],
    'flood': [0, 0, 255, 180],
    'earthquake': [165, 42, 42, 180]
}
df_selection['color'] = df_selection['type'].map(disaster_color_map)

view_state = pdk.ViewState(
    latitude=df_selection['lat'].mean() if not df_selection.empty else 0,
    longitude=df_selection['long'].mean() if not df_selection.empty else 0,
    zoom=1,
    pitch=50
)

layer = pdk.Layer(
    'ScatterplotLayer',
    data=df_selection,
    get_position='[long, lat]',
    get_radius ='intensity * 50000',
    get_color='color',
    pickable=True,
    auto_highlight=True
)

st.pydeck_chart(pdk.Deck(
map_style='mapbox://styles/mapbox/light-v9',
initial_view_state=view_state,
layers=[layer]
))

st.header("Filtered Data")
st.dataframe(df_selection)
