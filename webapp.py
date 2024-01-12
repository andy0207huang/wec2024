# ---WEBAPP---
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

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
# # TABLE
st.header("Scraped Data")
st.dataframe(df_selection)