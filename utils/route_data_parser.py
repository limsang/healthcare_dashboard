import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
# import plotly.graph_objs as go
# import gmplot
import glob
import sys
# from gpx_converter import Converter
import os
import haversine
from pandas import DataFrame


ROOT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))  # 상위 디렉토리
# ROOT_DIRECTORY = os.path.abspath(os.path.join(ROOT_DIRECTORY, os.pardir))

def gen_file_path(dir):
    """
    상위경로에서 data/~를 가져오도록
    """
    try:
        file_name = f"data/{dir}.csv"
        res = os.path.join(os.path.dirname(__file__), file_name)
        return res

    except Exception as e:
        print("error at gen_file_path", e)
        return -1

class RouteDataExtractor(object):

    def __init__(self, LOCATION):
        self.LOCATION = LOCATION
        # self.FILENAME = "route_2021-01-07_9.04pm.gpx"
        # self.gpx_file_name = LOCATION + self.FILENAME
        self.gpxHandler = None

    def loop_genDF(self):

        """
        모든 gpx 운동기록을 한꺼번에 저장하고 출력한다.
        입력은 리스트 형태의 gpx 자료들..
        :return:
        """

        file_list = glob.glob(self.LOCATION)
        print("file_list", file_list)
        file_list = [file for file in file_list if file.endswith(".gpx")]

        lst_gpxPool = list()
        for gpxfileName in file_list:
            self.gpxHandler = gpxpy.parse(open(gpxfileName))
            lst_gpxPool.append(self.gen_MassRouteDF(self.gpxHandler))
        df = pd.concat(lst_gpxPool)

        data_dir = os.path.join(ROOT_DIRECTORY, 'data/workout-routes/stacked_route_data.csv')
        df.to_csv(data_dir)  # file path, f
        print('for generating all cardio workouts')

    def gen_MassRouteDF(self, gpxHandler):

        """
        we need to create a variable that calculates our movement in meters per second
        with haversine 2d distance, since that’s the closest approximation of the distance proposed by the app.
        :return:
        """
        alt_dif = [0]
        time_dif = [0]
        dist_hav = [0]
        dist_hav_no_alt = [0]
        dist_dif_hav_2d = [0]
        columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']

        track = gpxHandler.tracks[0]
        segment = track.segments[0]
        data = []

        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude, point.elevation,
                         point.time, segment.get_speed(point_idx)])

        df = DataFrame(data, columns=columns)
        # 이동거리 및 시간 계산
        for index in range(len(data)):
            if index == 0:
                pass

            else:
                start = data[index-1]
                stop = data[index]

                distance_hav_2d = haversine.haversine((start[1], start[0]), (stop[1], stop[0]))*1000
                dist_dif_hav_2d.append(distance_hav_2d)
                dist_hav_no_alt.append(dist_hav_no_alt[-1] + distance_hav_2d)
                alt_d = start[2] - stop[2]
                alt_dif.append(alt_d)
                distance_hav_3d = sqrt(distance_hav_2d**2 + (alt_d)**2)
                time_delta = (stop[3] - start[3]).total_seconds()
                time_dif.append(time_delta)
                dist_hav.append(dist_hav[-1] + distance_hav_3d)

        df['dist_hav_2d'] = dist_hav_no_alt
        df['dis_hav_3d'] = dist_hav
        df['alt_dif'] = alt_dif
        df['time_dif'] = time_dif
        df['dis_dif_hav_2d'] = dist_dif_hav_2d

        df['dist_dif_per_sec'] = df['dis_dif_hav_2d'] / df['time_dif'] # 초속
        df['speed_km_per_hour'] = (df['dis_dif_hav_2d'] / df['time_dif']) * 3.6 # km/h.

        # we filter out all the data where the movement per second is larger than 90 centimeters
        df = df[df['dist_dif_per_sec'] > 0.9]

        # 결측값 모두 0으로 대체하여 그래프를 그린다.
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        # 수정후의 데이터프레임이 empty
        if len(df.index) == 0:
            return None

        return df


if __name__ == '__main__':
    data_dir = os.path.join(ROOT_DIRECTORY, 'data/workout-routes/*')
    # data_dir = gen_file_path("data/workout-routes/*")
    print("data_dir", data_dir)
    handler = RouteDataExtractor(data_dir)
    handler.loop_genDF()

