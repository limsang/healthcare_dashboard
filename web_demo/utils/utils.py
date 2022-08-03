import pytz
import pandas as pd
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))
get_year = lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month) #inefficient
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day) #inefficient
get_day = lambda x: convert_tz(x).day
get_month_only = lambda x: convert_tz(x).month
get_hour = lambda x: convert_tz(x).hour
get_minute = lambda x: convert_tz(x).minute
get_day_of_week = lambda x: convert_tz(x).weekday()
get_hour_min = lambda x: '{}-{:02}-{:02} {:02}:{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day, convert_tz(x).hour, convert_tz(x).min) #inefficient

def create_dataframe_with_initial_columns(df):
    """
    csv로 저장된 값을 df로 변환하는 역할
    """
    # parse out date and time elements as local time
    df['startDate'] = pd.to_datetime(df['startDate'])
    # parse to unix seconds since epoch
    df['timestamp'] = pd.to_datetime(df['startDate']).astype(int) / 10 ** 9 #view astype
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
    df['indexId'] = (df.index + 100).astype(str)
    df['dttm'] = df['startDate'].map(get_hour_min)
    df = df.fillna(value='')

    return df


def HeadphoneAudioExposure_splitter(data, index):
    res = data.split(',')
    res = res[index][6:]
    return res


def dbspl_norm(data):
    lst = [0, 30, 45, 60, 80, 90, 100, 9999999]
    color = ['mute', 'silence', 'whitenoise', 'cafenoise', 'stadium', 'rocking', 'kinda danger', 'warfare']

    res = "mute"
    for idx, item in enumerate(lst[:-1]):
        if lst[idx] < data <= lst[idx + 1]:
            res = color[idx + 1]

    return res
# if __name__ == '__main__':
#     path = "/Users/amore/Desktop/ap-gitlab/healthcare_dashboard/applewatch_data/BodyMass.csv"
#
#
