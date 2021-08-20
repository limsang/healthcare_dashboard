import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM
import pytz
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

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
def make_dataset(data, label, window_size=20):
    feature_list = []
    label_list = []
    for i in range(len(data) - window_size):
        feature_list.append(np.array(data.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size]))
    return np.array(feature_list), np.array(label_list)
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

if __name__ == '__main__':
    DistanceWalkingRunning = pd.read_csv('applewatch_data/DistanceWalkingRunning.csv')
    DistanceWalkingRunning = create_dataframe_with_initial_columns(DistanceWalkingRunning)

    left = DistanceWalkingRunning[['date', 'weekday_order']].drop_duplicates(['date'], keep='last')
    right = DistanceWalkingRunning[['value', 'date']]
    right = right.groupby(['date']).sum().reset_index()

    grp_running = pd.merge(left, right, left_on=['date'], right_on=['date'], how='inner')

    #아웃라이어 제거
    grp_running = grp_running.query('value < 15 and value > 1')



    scaler = MinMaxScaler()
    scale_cols = ['value', 'weekday_order']
    grp_running_scaled = scaler.fit_transform(grp_running[scale_cols])

    grp_running_scaled = pd.DataFrame(grp_running_scaled)
    grp_running_scaled.columns = scale_cols

    # for training, create train data
    TEST_SIZE = 50

    train = grp_running_scaled[:-TEST_SIZE]
    test = grp_running_scaled[-TEST_SIZE:]


    feature_cols = ['value','weekday_order']
    label_cols = ['value']

    train_feature = train[feature_cols]
    train_label = train[label_cols]

    # train dataset
    train_feature, train_label = make_dataset(train_feature, train_label, 5)
    # train, validation set 생성

    x_train, x_valid, y_train, y_valid= train_test_split(train_feature, train_label, test_size=0.2)

    x_train.shape, y_train.shape, x_valid.shape, y_valid.shape
    # ((236, 20, 2), (236, 1), (60, 20, 2), (60, 1))
    test_feature = train[feature_cols]
    test_label = train[label_cols]
    # test dataset (실제 예측 해볼 데이터)
    test_feature, test_label = make_dataset(test_feature, test_label, 7)


    tf.keras.backend.clear_session()

    model = Sequential()
    model.add(LSTM(units=32,  # dimensionality of the output space.
                   input_shape=(train_feature.shape[1], train_feature.shape[2]),  # 20, 4
                   activation='relu',
                   return_sequences=False)
              )
    model.add(Dense(1))

    print("model.summary()", model.summary())

    model.compile(loss='mean_squared_error', optimizer='adam')
    early_stop = EarlyStopping(monitor='val_loss', patience=5)
    filename = ('checkpoint.h5')
    checkpoint = ModelCheckpoint(filename, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')

    history = model.fit(x_train, y_train,
                        epochs=150,
                        batch_size=16,
                        validation_data=(x_valid, y_valid),
                        callbacks=[early_stop, checkpoint])

    # weight 로딩
    model.load_weights(filename)

    # 예측
    pred = model.predict(test_feature)

    plt.figure(figsize=(17, 9))
    plt.plot(test_label, label='actual')
    plt.plot(pred, label='prediction')
    plt.legend()
    plt.show()



