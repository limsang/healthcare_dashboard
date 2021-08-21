
from sklearn.model_selection import train_test_split
import pytz
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

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


def norm(df, col):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[col].max()
        min_value = df[col].min()
        result['norm_value'] = (df[col] - min_value) / (max_value - min_value)
    return result


def dbspl_norm(data):
    lst = [0, 30, 45, 60, 80, 90, 100, 9999999]
    color = ['mute', 'silence', 'whitenoise', 'cafenoise', 'stadium', 'rocking', 'kinda danger', 'warfare']

    res = "mute"
    for idx, item in enumerate(lst[:-1]):
        if lst[idx] < data <= lst[idx + 1]:
            res = color[idx + 1]

    return res


def HeadphoneAudioExposure_splitter(data, index):
    res = data.split(',')
    res = res[index][6:]
    return res


def make_dataset(data, label, n_steps_in, n_steps_out):
    offset = n_steps_in + n_steps_out
    feature_list = []
    label_list = []

    for i in range(len(data) - (offset)):
        feature_list.append(np.array(data.iloc[i:i + n_steps_in]))
        label_list.append(np.squeeze(np.array(label.iloc[i + n_steps_in:i + offset]), axis=1))

    return np.array(feature_list), np.array(label_list)


def main():
    moving_average_value = 50
    HeadphoneAudioExposure = pd.read_csv('applewatch_data/HeadphoneAudioExposure.csv')
    HeadphoneAudioExposure = create_dataframe_with_initial_columns(HeadphoneAudioExposure)

    HeadphoneAudioExposure['device_name'] = HeadphoneAudioExposure.apply(
        lambda x: HeadphoneAudioExposure_splitter(x["device"], 1), axis=1)
    HeadphoneAudioExposure = HeadphoneAudioExposure[['value', 'dttm', 'device_name', 'weekday', 'weekday_order']]
    HeadphoneAudioExposure = HeadphoneAudioExposure.groupby(["dttm", "device_name", "weekday", 'weekday_order']).max(
        ['value']).reset_index()
    HeadphoneAudioExposure['mv_avg'] = HeadphoneAudioExposure['value'].rolling(window=moving_average_value).mean()
    HeadphoneAudioExposure = HeadphoneAudioExposure.fillna(0)

    data = HeadphoneAudioExposure[['weekday_order', 'mv_avg', 'value']]
    n_steps_in, n_steps_out = 7, 5

    TEST_SIZE = int(0.2*len(data))

    train = data[:-TEST_SIZE]
    test = data[-TEST_SIZE:]

    feature_cols = ['value', 'weekday_order', 'mv_avg']
    label_cols = ['mv_avg']

    train_feature = train[feature_cols]
    train_label = train[label_cols]

    # lstm format
    train_feature, train_label = make_dataset(train_feature, train_label, n_steps_in, n_steps_out)

    # train, validation set 생성

    x_train, x_valid, y_train, y_valid = train_test_split(train_feature, train_label, test_size=0.2)

    n_features = x_train.shape[2]

    model = Sequential()
    model.add(LSTM(32, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
    model.add(LSTM(32, activation='relu'))
    model.add(Dense(n_steps_out))
    model.compile(optimizer='adam', loss='mse')

    early_stop = EarlyStopping(monitor='loss', patience=5)
    filename = ('multipredict.h5')
    checkpoint = ModelCheckpoint(filename, monitor='loss', verbose=1, save_best_only=True, mode='auto')

    history = model.fit(x_train, y_train,
                        epochs=50,
                        verbose=0,
                        batch_size=1,
                        validation_data=(x_valid, y_valid),
                        callbacks=[early_stop, checkpoint])

    test_feature = test[feature_cols]
    test_label = test[label_cols]
    # test dataset (실제 예측 해볼 데이터)

    test_feature, test_label = make_dataset(test_feature, test_label, n_steps_in, n_steps_out)
    # test_feature.shape, test_label.shape

    # weight 로딩
    model.load_weights(filename)

    # 예측
    pred = model.predict(test_feature)
    plt.figure(figsize=(17, 9))
    plt.plot(test_label, label='actual')
    plt.plot(pred, label='prediction')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()