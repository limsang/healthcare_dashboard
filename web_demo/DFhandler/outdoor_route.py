from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns
import os
import streamlit as st
import pytz

convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
get_hour = lambda x: '{}-{:02}-{:02} {:02}:{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day, convert_tz(x).hour, convert_tz(x).min) #inefficient


class OutdoorRoute(BaseHandler):

    @st.cache
    def load_from_csv(self, ROOT_DIRECTORY):
        travel_log = pd.read_csv(ROOT_DIRECTORY)
        travel_log = travel_log[['Latitude', 'Longitude', 'Time']]
        travel_log["Time"] = pd.to_datetime(travel_log['Time']).map(get_hour)
        travel_log['date_in_str'] = travel_log['Time'].astype(str)
        travel_log["date"] = pd.to_datetime(travel_log["Time"])
        travel_log.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

        return travel_log

    def preproc(self):
        pass

    def analysis_with_model(self):
        pass
    def visualize(self):
        pass