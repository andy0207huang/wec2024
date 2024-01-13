# ---WEBAPP---
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk


st.set_page_config(
    page_title="WEC 2024 - Natural Disaster",
    page_icon=":bar_chart:",
    layout="centered"
)

dfcsv = pd.read_csv("MOCK_DATA.csv")

# DASHBOARD
st.title(":bar_chart: Natural Disaster Webapp")
st.markdown("##")


# ========
# # FILTER
st.sidebar.header("Select the -Disaster Name- Filter Here:")

disasterName = st.sidebar.multiselect(
    "Select the Disaster Name:",
    options=dfcsv["Name"].unique(),
    default=dfcsv["Name"].unique()
)

df_selection = dfcsv.query(
    "Name == @disasterName"
)


# # --dynamic--
# MAP
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
st.header("Scraped Data")
st.dataframe(df_selection)