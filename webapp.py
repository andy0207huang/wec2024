# ---WEBAPP---
import pandas as pd
import streamlit as st

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

# Sidebar - Filter
st.sidebar.header("Select the -Disaster Name- Filter Here:")
disasterName = st.sidebar.multiselect(
    "Select the Disaster Name:",
    options=dfcsv["Name"].unique(),
    default=dfcsv["Name"].unique()
)

# Adding new disaster entry
st.header("Add New Disaster Event")
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
