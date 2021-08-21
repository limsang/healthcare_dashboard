import streamlit as st
import pandas as pd
from datetime import datetime
from folium.plugins import HeatMap
import folium
from streamlit_folium import folium_static
from dotenv import load_dotenv # python-dotenv
import os

ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # 상위 디렉토리
# ROOT_DIRECTORY = os.path.abspath(os.path.join(ROOT_DIRECTORY, os.pardir))
from DFhandler.outdoor_route import OutdoorRoute

import pytz
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
get_hour = lambda x: '{}-{:02}-{:02} {:02}:{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day, convert_tz(x).hour, convert_tz(x).min) #inefficient

def geo_workout(conf):
    #cache
    load_dotenv()
    outdoor_Route_HANDLER = OutdoorRoute()

    st.markdown("***")
    data_dir = os.path.join(ROOT_DIRECTORY,  conf.path['data']['outdoor_route_data'])
    travel_data = outdoor_Route_HANDLER.load_from_csv(data_dir)
    travel_data = outdoor_Route_HANDLER.preproc(travel_data)

    min_ts = datetime.strptime(min(travel_data["date_in_str"]), "%Y-%m-%d %H:%M")
    max_ts = datetime.strptime(max(travel_data["date_in_str"]), "%Y-%m-%d %H:%M")

    st.sidebar.subheader("Settings")
    min_selection, max_selection = st.sidebar.slider(
        "조회기간", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts]
    )

    # Toggles for the feature selection in sidebar
    show_heatmap = st.sidebar.checkbox("Show Heatmap")

    # Filter Data based on selection
    st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
    travel_data = travel_data[(travel_data["date"] >= min_selection) & (travel_data["date"] <= max_selection)]
    st.write(f"Data Points: {len(travel_data)}")

    # Plot the GPS coordinates on the map

    upperDF = travel_data.query('cluster == 1')
    upperDF = upperDF[['latitude','longitude','date','date_in_str']]
    lowerDF = travel_data.query('cluster == 0')

    st.map(upperDF)
    st.map(lowerDF)

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
