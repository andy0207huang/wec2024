# ---WEBAPP---
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
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


# ========
# # FILTER
st.sidebar.header("Select the -Disaster Name- Filter Here:")

with st.sidebar.expander("Filter by name:", expanded=True):
    disasterName = st.multiselect(
        "Select the Disaster Name:",
        options=dfcsv["Name"].unique(),
        default=dfcsv["Name"].unique()
    )
df_selection = dfcsv.query(
    "Name == @disasterName"
)

# # MAP
# If no disaster selected, show just the map
if disasterName:
    df_selection = dfcsv[dfcsv["Name"].isin(disasterName)]
else:
    df_selection = pd.DataFrame()

# MAP Default View
view_state = pdk.ViewState(
    latitude=df_selection['lat'].mean() if not df_selection.empty else 0,
    longitude=df_selection['long'].mean() if not df_selection.empty else 0,
    zoom=1,
    pitch=50
)

# MAP Colour map by Disaster "type"
disaster_color_map = {
    'tornado': [255, 255, 0, 180],  # Yellow
    'hurricane': [169, 169, 169, 180],  # Gray
    'flood': [0, 0, 255, 180],  # Blue
    'earthquake': [165, 42, 42, 180]  # Brown
}

df_selection['color'] = df_selection['type'].map(disaster_color_map)

# MAP Layer of label
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df_selection,
    get_position='[long, lat]',
    get_radius='intensity * 50000',
    get_color='color',
    pickable=True,
    auto_highlight=True,
    get_color_legend={
        "tornado": [255, 255, 0],
        "hurricane": [169, 169, 169],
        "flood": [0, 0, 255],
        "earthquake": [165, 42, 42]
    }
)

# SHOW MAP
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer]
))


# ========
# # TABLE RAW DATA
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

# Filter and display data
df_selection = dfcsv.query("Name == @disasterName")
st.header("Scraped Data")
st.dataframe(df_selection)
