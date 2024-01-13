# ---WEBAPP---
import pandas as pd
import streamlit as st
import pydeck as pdk
import altair as alt

from backend.dataHandle import getAllData, addRow, editData

## Set page configuration
st.set_page_config(
    page_title="WEC 2024 - Natural Disaster", page_icon="🌪️", layout="centered"
)

## LOAD CSV
path = "MOCK_DATA-OUTPUT.csv"
dfcsv = getAllData(open(path, "r"))

## TITLE
st.title("🌎🌊🌀🌪️ WEC2024")
st.title("Natural Disaster Dashboard")
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

# Sidebar - Filter by Country Name
with st.sidebar.expander("Filter by Country Name:", expanded=True):
    Countryname = st.multiselect(
        "Select the Country Name:",
        options=dfcsv["Country"].unique(),
        default=dfcsv["Country"].unique(),
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
        new_data = {
                    "Name": new_name,
                    "long": new_longitude,
                    "lat": new_latitude,
                    "date": new_date,
                    "intensity": new_intensity,
                    "type": new_type,
                }
        addRow(path, dfcsv, new_data)
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
    "Name == @disasterName & type == @disasterType & intensity >= @selected_intensity[0] & intensity <= @selected_intensity[1] & date >= @start_date & date <= @end_date & Country == @Countryname"
)


## DASHBOARD, THE MOST RECENT
st.markdown('### ❗❗ Most Recent Disaster ❗❗')
row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

most_recent_disaster = dfcsv.sort_values(by='date', ascending=False).head(1)

row1_col1.metric("Name", most_recent_disaster['Name'].values[0])
row1_col2.metric("Date", most_recent_disaster['date'].values[0])
row1_col3.metric("Type", most_recent_disaster['type'].values[0])
row1_col4.metric("Intensity", most_recent_disaster['intensity'].values[0])

row2_col1.metric("Longitude", most_recent_disaster['long'].values[0])
row2_col2.metric("Latitude", most_recent_disaster['lat'].values[0])
row2_col3.metric("Country", most_recent_disaster['Country'].values[0])




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

## REALTIME GRAPH
custom_color_scale = alt.Scale(domain=['tornado', 'hurricane', 'earthquake', 'flood'], range=['#FFFF00', '#A9A9A9', '#A52A2A', '#0000FF'])

# Graph - Vertical Stack Bar by YYYY-MM
st.header("Vertical Stack Bar of Counts of each Disaster Type by (YYYY-MM)")
# Aconvert date to YYYY-MM format string
df_selection['MonthYear'] = pd.to_datetime(df_selection['date']).dt.to_period('M').astype(str)
# Count each disaster type for each YYYY-MM
aggregated_data = pd.DataFrame(df_selection.groupby(['MonthYear', 'type']).size()).reset_index()
aggregated_data.columns = ['MonthYear', 'type', 'count']

vsb1 = alt.Chart(aggregated_data).mark_bar().encode(
    x='MonthYear:N',
    y='sum(count):Q',
    color=alt.Color('type:N', scale=custom_color_scale)
).properties(
    width=600,
    height=500
)

# Show GRAPH
st.altair_chart(vsb1, use_container_width=True)


# Graph - Vertical Stack Bar by COUNTRY
st.header("Vertical Stack Bar of Counts of each Disaster Type by (Country)")
# Count each disaster type by COUNTRY
aggregated_data_c = pd.DataFrame(df_selection.groupby(['Country', 'type']).size()).reset_index()
aggregated_data_c.columns = ['Country', 'type', 'count']

vsb2 = alt.Chart(aggregated_data_c).mark_bar().encode(
    x='Country:N',
    y='sum(count):Q',
    color=alt.Color('type:N', scale=custom_color_scale)
).properties(
    width=900,
    height=500
)

# Show GRAPH
st.altair_chart(vsb2, use_container_width=True)


# Graph - Vertical Stack Bar by INTENSITY
st.header("Vertical Stack Bar of Counts of each Disaster Type by (Intensity)")
# Count each disaster type by INTENSITY
aggregated_data_i = pd.DataFrame(df_selection.groupby(['intensity', 'type']).size()).reset_index()
aggregated_data_i.columns = ['intensity', 'type', 'count']

vsb3 = alt.Chart(aggregated_data_i).mark_bar().encode(
    x='intensity:N',
    y='sum(count):Q',
    color=alt.Color('type:N', scale=custom_color_scale)
).properties(
    width=900,
    height=500
)

# Show GRAPH
st.altair_chart(vsb3, use_container_width=True)

## RAW TABLE DATA
st.header("Data Table")
st.dataframe(df_selection)