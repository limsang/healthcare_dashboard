from datetime import date, datetime, timedelta as td
import pytz
import numpy as np
import pandas as pd
import json
from elasticsearch import Elasticsearch
from es_pandas import es_pandas
import sys

# instantiate elastic search
# es = Elasticsearch('192.168.0.7:9200')

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

  self.ES_PORT = '9200'
  self.IP = '192.168.0.7'
  self.es = Elasticsearch('192.168.0.7:9200')
  self.TYPE = 'record'

  self.es_host = 'localhost:9200'
  # crete es_pandas instance
  self.ep = es_pandas(self.es_host)


 def check_and_generate_index(self, INDEX):
  if self.es.indices.exists(INDEX):
   self.es.indices.delete(INDEX)
  # Create index
  self.es.indices.create(INDEX)

 def gen_step_index(self):

  steps = pd.read_csv("data/StepCount.csv")
  # parse out date and time elements as local time
  steps['startDate'] = pd.to_datetime(steps['startDate'])
  # parse to unix seconds since epoch
  steps['timestamp'] = pd.to_datetime(steps['startDate']).astype(int) / 10**9
  steps['dow'] = steps['startDate'].map(get_day_of_week)
  steps['year'] = steps['startDate'].map(get_year)
  steps['month'] = steps['startDate'].map(get_month)
  steps['date'] = steps['startDate'].map(get_date)
  steps['day'] = steps['startDate'].map(get_day)
  steps['hour'] = steps['startDate'].map(get_hour)
  steps['dow'] = steps['startDate'].map(get_day_of_week)
  dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
  steps['weekday'] = steps['startDate'].dt.dayofweek.map(dayOfWeek)
  steps['indexId'] = (steps.index + 100).astype(str)
  steps = steps.fillna(value='')

  INDEX = 'steps'
  self.check_and_generate_index(INDEX)


  # Add mapping
  with open('apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  self.ep.init_es_tmpl(steps, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(steps, INDEX, doc_type=self.TYPE)

 def gen_resting_index(self):
  resting = pd.read_csv("data/RestingHeartRate.csv")

  # parse out date and time elements as local time
  resting['startDate'] = pd.to_datetime(resting['startDate'])

  # parse to unix seconds since epoch
  resting['timestamp'] = pd.to_datetime(resting['startDate']).astype(int) / 10**9
  resting['dow'] = resting['startDate'].map(get_day_of_week)
  resting['year'] = resting['startDate'].map(get_year)
  resting['month'] = resting['startDate'].map(get_month)
  resting['date'] = resting['startDate'].map(get_date)
  resting['day'] = resting['startDate'].map(get_day)
  resting['hour'] = resting['startDate'].map(get_hour)
  resting['dow'] = resting['startDate'].map(get_day_of_week)
  dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
  resting['weekday'] = resting['startDate'].dt.dayofweek.map(dayOfWeek)

  resting['indexId'] = (resting.index + 100).astype(str)

  resting = resting.fillna(value='')

  INDEX = 'resting_hr'
  self.check_and_generate_index(INDEX)

  # Add mapping
  with open('apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  self.ep.init_es_tmpl(resting, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(resting, INDEX, doc_type=self.TYPE)

 def gen_heartRate_index(self):
  hr = pd.read_csv("data/HeartRate.csv")

  # parse out date and time elements as local time
  hr['startDate'] = pd.to_datetime(hr['startDate'])

  # parse to unix seconds since epoch
  hr['timestamp'] = pd.to_datetime(hr['startDate']).astype(int) / 10**9

  hr['dow'] = hr['startDate'].map(get_day_of_week)
  hr['year'] = hr['startDate'].map(get_year)
  hr['month'] = hr['startDate'].map(get_month)
  hr['date'] = hr['startDate'].map(get_date)
  hr['day'] = hr['startDate'].map(get_day)
  hr['hour'] = hr['startDate'].map(get_hour)
  hr['dow'] = hr['startDate'].map(get_day_of_week)

  dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
  hr['weekday'] = hr['startDate'].dt.dayofweek.map(dayOfWeek)

  hr['indexId'] = (hr.index + 100).astype(str)

  hr = hr.fillna(value='')

  INDEX = 'hr'

  self.check_and_generate_index(INDEX)

  # Add mapping
  with open('apple_health_elastic_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=INDEX, doc_type=self.TYPE, body=d, include_type_name=True)

  self.ep.init_es_tmpl(hr, self.TYPE)
  # Example of write data to es, use the template you create
  self.ep.to_es(hr, INDEX, doc_type=self.TYPE)

 def gen_workOut_index(self):
  Workout = pd.read_csv("data/Workout.csv")

  # parse out date and time elements as Shanghai time
  Workout['startDate'] = pd.to_datetime(Workout['startDate'])
  Workout['year'] = Workout['startDate'].map(get_year)
  Workout['month'] = Workout['startDate'].map(get_month)
  Workout['date'] = Workout['startDate'].map(get_date)
  Workout['day'] = Workout['startDate'].map(get_day)
  Workout['hour'] = Workout['startDate'].map(get_hour)
  Workout['dow'] = Workout['startDate'].map(get_day_of_week)

  dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
  Workout['weekday'] = Workout['startDate'].dt.dayofweek.map(dayOfWeek)
  Workout['indexId'] = (Workout.index + 100).astype(str)
  Workout = Workout.fillna(value='')

  cardio_mask=Workout['totalDistance']>0
  weight_trainig_mask=Workout['totalDistance'] == 0
  CardioWorkout = Workout[cardio_mask]
  weight_training= Workout[weight_trainig_mask]

  CARDIO_INDEX = 'cardioworkout'

  self.check_and_generate_index(CARDIO_INDEX)

  # Add mapping
  with open('apple_health_elastic_workout_mapping.json') as json_mapping:
   d = json.load(json_mapping)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=CARDIO_INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  # Example of write data to es, use the template you create
  self.ep.to_es(CardioWorkout, CARDIO_INDEX, doc_type=self.TYPE)

  MUSCULAR_INDEX = 'weighttraining'

  self.check_and_generate_index(MUSCULAR_INDEX)

  # Create Customized Index Mappings
  self.es.indices.put_mapping(index=MUSCULAR_INDEX, doc_type=self.TYPE, body=d, include_type_name=True)
  # Example of write data to es, use the template you create
  self.ep.to_es(weight_training, MUSCULAR_INDEX, doc_type=self.TYPE)

if __name__ == '__main__':
    handler = HealthDataExtractor()
    handler.gen_resting_index()
