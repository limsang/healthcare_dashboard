import gpxpy
import matplotlib.pyplot as plt
import datetime
from geopy import distance
from math import sqrt, floor
import numpy as np
import pandas as pd
# import plotly.plotly as py -> deprecated
import plotly.graph_objs as go
import haversine
# from gpx_converter import Converter
from pandas import DataFrame

class HealthDataExtractor(object):

    def __init__(self):
        self.gpx_file_name = "route_2020-10-04_2.23pm.gpx"
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
        df.count()

        """
        I want to plot the direction of the movement with a quiver plot. For that I will need the u and v velocity components. And to compute u and v I need the angle associated to each speed data. Instead of re-inventing the wheel I will use the seawater library sw.dist function to calculate the angles.
        
        I also smoothed the data a little bit to improve the plot. (GPX data from smart-phones can be very noisy.)
        
        -> 나라시 깔겠다고..
        
        No module named 'oceans.ff_tools' error
        """
        # import seawater as sw
        # from oceans.ff_tools import smoo1

        # _, angles = sw.dist(df['Latitude'], df['Longitude'])
        # angles = np.r_[0, np.deg2rad(angles)]

        # # Normalize the speed to use as the length of the arrows
        # r = df['Speed'] / df['Speed'].max()
        # kw = dict(window_len=31, window='hanning')
        # df['u'] = smoo1(r * np.cos(angles), **kw)
        # df['v'] = smoo1(r * np.sin(angles), **kw)
        # df.head()





