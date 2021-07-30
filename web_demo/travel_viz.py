import streamlit as st
import pandas as pd
from datetime import datetime
from folium.plugins import HeatMap
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import flickrapi
import random
from dotenv import load_dotenv # python-dotenv
import os
import urllib

from utils.route_data_parser import RouteDataExtractor

def uploadGPX_saveCSV():
    log_file_in_xml = st.file_uploader("Upload XML", type=['gpx'])
    if st.button("xml데이터 저장"):
        tmp = "route.gpx"
        XML_PATH = f'data/workout-routes/{tmp}'
        """
        업로드한 파일을 지정된 경로로 복사한다.
        """
        # "data/workout-routes/*"
        # if log_file_in_xml is not None:
        #     data = RouteDataExtractor(XML_PATH)
        #     data.loop_genDF()
        #
        # else:
        #     st.info("not an valid file")

    def file_selector(folder_path='/'):
        val = folder_path
        # /Users/amore/Desktop/ap-gitlab/healthcare_dashboard/web_demo/data/workout-routes
        val = st.text_input("type in absolute workout-route path")
        print(val)
        selected_filename = st.selectbox('Select a file', val)
        return val


def geo_workout():
    load_dotenv()

    #@st.cache
    def load_data():
        """ Load the cleaned data with latitudes, longitudes & timestamps """
        travel_log = pd.read_csv("result.csv")
        travel_log["date"] = pd.to_datetime(travel_log["date_2"])
        travel_log.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)
        return travel_log

    # uploadGPX_saveCSV()
    st.markdown("***")

    travel_data = load_data()

    min_ts = datetime.strptime(min(travel_data["date_3"]), "%Y-%m-%d %H:%M")
    max_ts = datetime.strptime(max(travel_data["date_3"]), "%Y-%m-%d %H:%M")

    st.sidebar.subheader("Inputs")
    min_selection, max_selection = st.sidebar.slider(
        "Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts]
    )

    # Toggles for the feature selection in sidebar
    show_heatmap = st.sidebar.checkbox("Show Heatmap")

    # Filter Data based on selection
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
    travel_data = travel_data[(travel_data["date"] >= min_selection) & (travel_data["date"] <= max_selection)]
    st.write(f"Data Points: {len(travel_data)}")

    # Plot the GPS coordinates on the map
    st.map(travel_data)

    if show_heatmap:
        # Plot the heatmap using folium. It is resource intensive!
        # Set the map to center around Munich, Germany (48.1351, 11.5820)
        map_heatmap = folium.Map(location=[37.518766, 126.97120600000001], zoom_start=11)

        # Filter the DF for columns, then remove NaNs
        heat_df = travel_data[["latitude", "longitude"]]
        heat_df = heat_df.dropna(axis=0, subset=["latitude", "longitude"])

        # List comprehension to make list of lists
        heat_data = [
            [row["latitude"], row["longitude"]] for index, row in heat_df.iterrows()
        ]

        # Plot it on the map
        HeatMap(heat_data).add_to(map_heatmap)

        # Display the map using the community component
        st.subheader("Heatmap")
        folium_static(map_heatmap)
