import pytz
import pandas as pd
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles'))
get_year = lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month) #inefficient
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day) #inefficient
get_day = lambda x: convert_tz(x).day
get_hour = lambda x: convert_tz(x).hour
get_minute = lambda x: convert_tz(x).minute
get_day_of_week = lambda x: convert_tz(x).weekday()


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
    df['date'] = df['startDate'].map(get_date)
    df['day'] = df['startDate'].map(get_day)
    df['hour'] = df['startDate'].map(get_hour)
    df['dow'] = df['startDate'].map(get_day_of_week)
    dayOfWeek = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    df['weekday'] = df['startDate'].dt.dayofweek.map(dayOfWeek)
    df['indexId'] = (df.index + 100).astype(str)
    df = df.fillna(value='')

    return df