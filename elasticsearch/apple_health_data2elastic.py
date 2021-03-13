from datetime import date, datetime, timedelta as td
import pytz
import numpy as np
import pandas as pd
import json
from elasticsearch import Elasticsearch
from es_pandas import es_pandas
import sys
import json

# functions to convert UTC to Shanghai time zone and extract date/time elements
convert_tz = lambda x: x.to_pydatetime().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('America/Los_Angeles'))
get_year = lambda x: convert_tz(x).year
get_month = lambda x: '{}-{:02}'.format(convert_tz(x).year, convert_tz(x).month) #inefficient
get_date = lambda x: '{}-{:02}-{:02}'.format(convert_tz(x).year, convert_tz(x).month, convert_tz(x).day) #inefficient
get_day = lambda x: convert_tz(x).day
get_hour = lambda x: convert_tz(x).hour
get_minute = lambda x: convert_tz(x).minute
get_day_of_week = lambda x: convert_tz(x).weekday()


class HealthDataExtractor(object):
 def __init__(self):
  with open('config.json', 'r') as f:
    self.config = json.load(f)

  self.ES_PORT = self.config["ES_PORT"]
  self.IP = self.config["ES_IP"]
  self.es = Elasticsearch(f"{self.IP}:{self.ES_PORT}", verify_certs=True)

  if not self.es.ping():
    raise ValueError("Connection failed")

  else:
   print("elasticsearch connection... ping result....", self.es.ping())

  self.TYPE = self.config["TYPE"]
  self.ep = es_pandas(f"{self.IP}:{self.ES_PORT}")

 def check_and_generate_index(self, INDEX):
  if self.es.indices.exists(INDEX):
   self.es.indices.delete(INDEX)
  # Create index
  self.es.indices.create(INDEX)

 def create_dafareame_with_initial_columns(self, csv_path):

  df = pd.read_csv(csv_path)

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

 def gen_step_index(self):

  steps = self.create_dafareame_with_initial_columns("data/StepCount.csv")
  INDEX = 'steps'
  self.check_and_generate_index(INDEX)

  # Add mapping
  with open('index_mappings/apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  self.ep.init_es_tmpl(steps, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(steps, INDEX, doc_type=self.TYPE)

 def gen_resting_index(self):

  resting = self.create_dafareame_with_initial_columns("data/RestingHeartRate.csv")

  INDEX = 'resting_hr'
  self.check_and_generate_index(INDEX)

  # Add mapping
  with open('index_mappings/apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  self.ep.init_es_tmpl(resting, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(resting, INDEX, doc_type=self.TYPE)

 def gen_heartRate_index(self):

  hr = self.create_dafareame_with_initial_columns("data/HeartRate.csv")
  INDEX = 'hr'

  self.check_and_generate_index(INDEX)

  # Add mapping
  with open('index_mappings/apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)

  self.ep.init_es_tmpl(hr, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(hr, INDEX, doc_type=self.TYPE)

 def gen_workOut_index(self):
  """
  workout csv를 통해 여러 타입의 운동관련 인덱스를 생성한다.
  :return: 유 무산소 운동기록에 대한 인덱스
  """
  Workout = self.create_dafareame_with_initial_columns("data/Workout.csv")
  cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

  """
  요일별 운동횟수를 기록
  
  """
  weekdayCount = Workout
  weekdayCount = weekdayCount[['weekday']].groupby(weekdayCount['weekday'])


  #유산소 운동
  cardio_mask=Workout['totalDistance'] > 0
  CardioWorkout = Workout[cardio_mask]
  CardioWorkout['ExerciseIntensity'] = round(CardioWorkout['totalEnergyBurned'] / CardioWorkout['duration'])
  CardioWorkout['date'] = pd.to_datetime(CardioWorkout['date'])
  CardioWorkout = CardioWorkout[['date', 'weekday', 'duration', 'totalEnergyBurned', 'ExerciseIntensity']]
  CardioWorkout = CardioWorkout.set_index('date')

  #무산소 운동
  weight_trainig_mask=Workout['totalDistance'] == 0
  weight_training= Workout[weight_trainig_mask]
  # 운동강도 추가
  weight_training['ExerciseIntensity'] = round(weight_training['totalEnergyBurned'] / weight_training['duration'])

  gymTraining = weight_training
  gymTraining['date'] = pd.to_datetime(weight_training['date'])
  gymTraining = gymTraining[['date', 'weekday', 'duration', 'totalEnergyBurned', 'ExerciseIntensity']]
  gymTraining = gymTraining.set_index('date')

  # 요일별 운동량을 측정한다.
  gymTrainingPerWeekday = gymTraining[['duration', 'totalEnergyBurned', 'ExerciseIntensity']].groupby(gymTraining['weekday'])
  gymTrainingPerWeekday = gymTrainingPerWeekday.mean().reindex(cats)
  # 인덱스를 일반 컬럼으로 이동
  gymTrainingPerWeekday = gymTrainingPerWeekday.reset_index()

  self.dataframe_to_es(CardioWorkout, 'cardioworkout', 'apple_health_elastic_cardio_workout_mapping.json')
  self.dataframe_to_es(gymTraining, 'weighttraining', 'apple_health_elastic_workout_mapping.json')
  self.dataframe_to_es(gymTrainingPerWeekday, 'weighttraining_week', 'apple_health_elastic_workout_week_mapping.json')

 def dataframe_to_es(self, dataframe, index_name, mapping_json):
  INDEX = index_name
  self.check_and_generate_index(INDEX)

  # Add mapping
  with open(mapping_json) as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  # Example of write data to es, use the template you create
  self.ep.to_es(dataframe, INDEX, doc_type=self.TYPE)

if __name__ == '__main__':
    handler = HealthDataExtractor()
    handler.gen_heartRate_index()
    handler.gen_resting_index()
