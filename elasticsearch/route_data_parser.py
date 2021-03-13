import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import gmplot
from gpx_converter import Converter
import os
import haversine
# from gpx_converter import Converter
from pandas import DataFrame

class HealthDataExtractor(object):

    def __init__(self):
        self.gpx_file_name = "data/workout-routes/route_2020-12-15_4.14pm.gpx"
        self.gpx = gpxpy.parse(open(self.gpx_file_name))

    def gen_routeDF(self):
        print("{} track(s)".format(len(self.gpx.tracks)))
        track = self.gpx.tracks[0]

        print("{} segment(s)".format(len(track.segments)))
        segment = track.segments[0]

        print("{} point(s)".format(len(segment.points)))
        data = []

        segment_length = segment.length_3d()

        for point_idx, point in enumerate(segment.points):
            data.append([point.longitude, point.latitude, point.elevation, point.time, segment.get_speed(point_idx)])

        columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
        df = DataFrame(data, columns=columns)

        alt_dif = [0]
        time_dif = [0]
        dist_hav = [0]
        dist_hav_no_alt = [0]
        dist_dif_hav_2d = [0]

        """
        이동거리 및 시간 계산
        """
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

        # we need to create a new variable that calculates our movement in meters per second
        # with haversine 2d distance, since that’s the closest approximation of the distance proposed by the app.
        df['dist_dif_per_sec'] = df['dis_dif_hav_2d'] / df['time_dif'] # 초속
        """
        we might as well calculate the speed for every data point. 
        First, we create a new column in our dataframe named speed.
        This new variable is calculated by dividing the distance traveled in meters by the time it took in seconds, 
        and then converted to km/h.
        """
        df['speed_km_per_hour'] = (df['dis_dif_hav_2d'] / df['time_dif']) * 3.6

        """
        we filter out all the data where the movement per second is larger than 90 centimeters 
        (see section above for the reason).
        """
        df = df[df['dist_dif_per_sec'] > 0.9]

        """
        We can therefore conclude that if the movement per seconde was less than 80 centimeters, 
        the application didn’t consider it as a movement and stopped the timer. 
        초당 80센치 미만으로 이동하면 이동안한걸로 간주하겠다는 말씀
        """
        # for treshold in [0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        #     print(treshold, 'm', ' : Time:', sum(df[df['dist_dif_per_sec'] < treshold]['time_dif']), ' seconds')

        # 결측값 모두 0으로 대체하여 그래프를 그린다.
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)

        # 1키로미터 이동하는데에 걸리는 평균 시간
        avg_km_h = (sum((df['speed_km_per_hour'] * df['time_dif'])) / sum(df['time_dif']))
        print("1키로미터 이동하는데에 걸리는 평균 시간", floor(60 / avg_km_h), 'minutes', round(((60 / avg_km_h - floor(60 / avg_km_h))*60), 0), ' seconds')
        df['time10s'] = list(map(lambda x: round(x, -1), np.cumsum(df['time_dif'])))

        # speed in km/h against the time in seconds.
        # plt.plot(df.groupby(['time10s']).mean()['spd'])

        print('Haversine 2D : ', dist_hav_no_alt[-1]*0.001, "km")
        print('Haversine 3D : ', dist_hav[-1]*0.001, "km")
        print('Total Time : ', floor(sum(time_dif)/60),' min ', int(sum(time_dif)%60),' sec ')

        # simpleDF = Converter(input_file=self.gpx_file_name).gpx_to_dataframe()

        min_lat, max_lat, min_lon, max_lon = \
            min(df['Latitude']), max(df['Latitude']), \
            min(df['Longitude']), max(df['Longitude'])
        # Create empty map with zoom level 16
        mymap = gmplot.GoogleMapPlotter(
            min_lat + (max_lat - min_lat) / 2,
            min_lon + (max_lon - min_lon) / 2,
            16)

        mymap.plot(df['Latitude'], df['Longitude'], 'red', edge_width=3, maptype="satellite")
        mymap.draw('my_gm_plot10.html')

if __name__ == '__main__':
    handler = HealthDataExtractor()
    handler.gen_routeDF()
