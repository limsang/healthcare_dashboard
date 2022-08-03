from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns
import os
from sklearn.cluster import KMeans
import streamlit as st
import pytz
import numpy as np
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
get_hour = lambda x: '{}-{:02}-{:02} {:02}:{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day, convert_tz(x).hour, convert_tz(x).min) #inefficient


class OutdoorRoute(BaseHandler):

    @st.cache
    def load_from_csv(self, ROOT_DIRECTORY):
        try:
            travel_log = pd.read_csv(ROOT_DIRECTORY)
            travel_log = travel_log[['Latitude', 'Longitude', 'speed_km_per_hour', 'Speed', 'Time']]
            travel_log["Time"] = pd.to_datetime(travel_log['Time']).map(get_hour)
            travel_log['date_in_str'] = travel_log['Time'].astype(str)
            travel_log["date"] = pd.to_datetime(travel_log["Time"])

            travel_log['row_number'] = np.arange(len(travel_log))
            travel_log.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

            return travel_log
        except Exception as e:
            print("errrrrr",e )

    def preproc(self, route):
        _route = route
        kmeans = KMeans(n_clusters=2)
        # kmeans.fit(route[['dist_dif_per_sec','Longitude','Latitude']])

        kmeans.fit(route[['Speed', 'latitude', 'longitude', 'speed_km_per_hour']])

        # 결과 확인
        result_by_sklearn = route.copy()
        result_by_sklearn["cluster"] = kmeans.labels_

        cluster = pd.DataFrame(np.array([kmeans.labels_]).T)
        cluster.columns = ['cluster']
        cluster = cluster.reset_index()

        sfs_result = pd.merge(_route, cluster, left_on=['row_number'], right_on=['index'], how='inner')

        # sfs_result = sfs_result.query('cluster == 1')
        # print("cluster", sfs_result.iloc[0])
        return sfs_result

    def analysis_with_model(self):
        pass

    def visualize(self):
        pass