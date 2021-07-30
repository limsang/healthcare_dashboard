import gpxpy
from math import sqrt, floor
import numpy as np
import pandas as pd
import glob
import sys
import haversine
from pandas import DataFrame

class HealthDataExtractor(object):

    def __init__(self):
        LOCATION = "data/workout-routes/"
        self.FILENAME = "route_2021-01-07_9.04pm.gpx"
        self.gpx_file_name = LOCATION + self.FILENAME
        self.gpxHandler = gpxpy.parse(open(self.gpx_file_name))
        # self.gen_routeDF(self.gpxHandler, self.FILENAME)

    def loop_genDF(self):

        """
        모든 gpx 운동기록을 한꺼번에 저장하고 출력한다.
        입력은 리스트 형태의 gpx 자료들..
        :return:
        """

        path = "data/workout-routes/*"
        file_list = glob.glob(path)
        file_list = [file for file in file_list if file.endswith(".gpx")]
        print("file_list", file_list)

        lst_gpxPool = list()
        for gpxfileName in file_list:
            self.gpxHandler = gpxpy.parse(open(gpxfileName))
            # self.gen_routeDF(self.gpxHandler, gpxfileName)
            lst_gpxPool.append(self.gen_MassRouteDF(self.gpxHandler))
        df = pd.concat(lst_gpxPool)
        df.to_csv(f'dsafsdf.csv')  # file path, f
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

    def gen_routeDF(self, gpxHandler, filename):

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

        print("filename", filename)
        print("{} track(s)".format(len(gpxHandler.tracks)))
        track = gpxHandler.tracks[0]

        print("{} segment(s)".format(len(track.segments)))
        segment = track.segments[0]

        print("{} point(s)".format(len(segment.points)))

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
            print("empty dataframe!!")
            return

        # 1키로미터 이동하는데에 걸리는 평균 시간
        try:
            avg_km_h = (sum((df['speed_km_per_hour'] * df['time_dif'])) / sum(df['time_dif']))
        except ZeroDivisionError as e:
            print("error!!!!! ---", df['time_dif'])
            print(df)
            sys.exit()
        # return df
        print("filename", filename)
        df.to_csv(f'dsafsdf.csv')  # file path, f
        print("1키로미터 이동하는데에 걸리는 평균 시간", floor(60 / avg_km_h), 'minutes', round(((60 / avg_km_h - floor(60 / avg_km_h))*60), 0), ' seconds')

        # speed in km/h against the time in seconds.
        # df['time10s'] = list(map(lambda x: round(x, -1), np.cumsum(df['time_dif'])))
        # plt.plot(df.groupby(['time10s']).mean()['spd'])

        print('Haversine 2D : ', dist_hav_no_alt[-1]*0.001, "km")
        print('Haversine 3D : ', dist_hav[-1]*0.001, "km")
        print('Total Time : ', floor(sum(time_dif)/60),' min ', int(sum(time_dif)%60),' sec ')
        print("----------------------------")
        # self.draw_on_google_map(df)

    # def draw_on_google_map(self, df):
    #     min_lat, max_lat, min_lon, max_lon = min(df['Latitude']), max(df['Latitude']), min(df['Longitude']), max(df['Longitude'])
    #     # Create empty map with zoom level 16
    #     mymap = gmplot.GoogleMapPlotter( min_lat + (max_lat - min_lat) / 2, min_lon + (max_lon - min_lon) / 2, 16)
    #
    #     mymap.plot(df['Latitude'], df['Longitude'], 'red', edge_width=3, maptype="satellite")
    #     mymap.draw(self.FILENAME + '.html')

if __name__ == '__main__':
    handler = HealthDataExtractor()

    # path = "data/workout-routes"
    handler.loop_genDF()

