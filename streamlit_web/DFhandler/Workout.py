from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns

class Workout(BaseHandler):

    def load_from_csv(self, df):
        _df = create_dataframe_with_initial_columns(df)
        return _df

    def preproc(self, Workout):
        cats = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        """
        요일별 운동횟수를 기록

        """
        weekdayCount = Workout
        weekdayCount = weekdayCount[['weekday']].groupby(weekdayCount['weekday'])

        # 유산소 운동
        cardio_mask = Workout['totalDistance'] > 0
        CardioWorkout = Workout[cardio_mask]
        CardioWorkout['ExerciseIntensity'] = round(CardioWorkout['totalEnergyBurned'] / CardioWorkout['duration'])
        CardioWorkout['date'] = pd.to_datetime(CardioWorkout['date'])
        CardioWorkout = CardioWorkout[['date', 'weekday', 'duration', 'totalEnergyBurned', 'ExerciseIntensity']]
        CardioWorkout = CardioWorkout.set_index('date')

        # 무산소 운동
        weight_trainig_mask = Workout['totalDistance'] == 0
        weight_training = Workout[weight_trainig_mask]
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

        return CardioWorkout, gymTraining, gymTrainingPerWeekday

    def analysis_with_model(self):
        pass

    def visualize(self, df):
        pass
