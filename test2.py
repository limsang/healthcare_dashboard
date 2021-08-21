
import pytz

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
get_year = lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month)  # inefficient
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day)  # inefficient
get_day = lambda x: convert_tz(x).day
get_month_only = lambda x: convert_tz(x).month
get_hour = lambda x: convert_tz(x).hour
get_minute = lambda x: convert_tz(x).minute
get_day_of_week = lambda x: convert_tz(x).weekday()

get_hour_min = lambda x: '{}-{:02}-{:02} {:02}:{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day,
                                                             convert_tz(x).hour, convert_tz(x).min)  # inefficient


def create_dataframe_with_initial_columns(df):
    """
    csv로 저장된 값을 df로 변환하는 역할
    """
    # parse out date and time elements as local time
    df['startDate'] = pd.to_datetime(df['startDate'])
    # parse to unix seconds since epoch
    df['timestamp'] = pd.to_datetime(df['startDate']).astype(int) / 10 ** 9
    df['dow'] = df['startDate'].map(get_day_of_week)
    df['year'] = df['startDate'].map(get_year)
    df['month'] = df['startDate'].map(get_month)
    df['month_only'] = df['startDate'].map(get_month_only)
    df['date'] = df['startDate'].map(get_date)
    df['day'] = df['startDate'].map(get_day)
    df['hour'] = df['startDate'].map(get_hour)
    df['dow'] = df['startDate'].map(get_day_of_week)
    dayOfWeek = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['weekday'] = df['startDate'].dt.dayofweek.map(dayOfWeek)
    df['weekday_order'] = df['startDate'].dt.dayofweek
    df['indexId'] = (df.index + 100).astype(str)
    df['dttm'] = df['startDate'].map(get_hour_min)
    df = df.fillna(value='')

    return df


def main():
    df = pd.read_csv('applewatch_data/workout-routes/stacked_route_data.csv')
    df = create_dataframe_with_initial_columns(df)

    empty_date = df.groupby("date").max().reset_index()
    r = pd.date_range(start=empty_date.date.min(), end=empty_date.date.max())
    empty_date = empty_date.set_index('date').reindex(r).fillna(0.0).rename_axis('date').reset_index()
    empty_date = empty_date[~empty_date.date.isin(df.date)]
    frames = [df, empty_date, None]
    df = pd.concat(frames)

    overall = df[['duration', 'workoutActivityType', 'totalEnergyBurned', 'date']]  # .query('duration>0')
    overall['date'] = pd.to_datetime(overall['date'])
    overall['date'] = overall['date'].astype(str)
    overall['workoutActivityType'].replace({0: "NULL"}, inplace=True)

    # k에 따라 inertia_(군집 내 거리제곱합의 합)이 어떻게 변하는 지 시각화
    def change_n_clusters(n_clusters, data):
        sum_of_squared_distance = []
        for n_cluster in n_clusters:
            kmeans = KMeans(n_clusters=n_cluster)
            kmeans.fit(data)
            sum_of_squared_distance.append(kmeans.inertia_)

        plt.figure(1, figsize=(12, 6))
        plt.plot(n_clusters, sum_of_squared_distance, 'o')
        plt.plot(n_clusters, sum_of_squared_distance, '-', alpha=0.5)
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')

if __name__ == '__main__':
    main()