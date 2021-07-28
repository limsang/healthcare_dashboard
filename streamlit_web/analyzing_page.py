import streamlit as st
import pandas as pd

from utils.utils import create_dataframe_with_initial_columns

from DFhandler.HeartRate import HeartRate
from DFhandler.Workout import Workout
from DFhandler.StepCount import StepCount
from DFhandler.RestingHeartRate import RestingHeartRate


VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
 'AppleStandTime.csv']


def Dataset():
    RHR_HANDLER = RestingHeartRate()
    Workout_HANDLER = Workout()
    StepCount_HANDLER = StepCount()
    HeartRate_HANDLER = HeartRate()

    tmp = None
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV", type=['csv'])

    if st.button("Process"):
        if data_file is not None:
            if data_file.name in VALID_FILE_LIST:
                st.write("valid file name")
                # show file details
                file_details = {"Filename": data_file.name, "FileType": data_file.type,"FileSize":data_file.size}
                st.write(file_details)
                df = pd.read_csv(data_file)
                st.dataframe(df.head(10))

                # 업로드한 파일명을 기준으로 분석

                if data_file.name == 'Workout.csv':
                    tmp = Workout_HANDLER.load_from_csv(df)
                    CardioWorkout, gymTraining, gymTrainingPerWeekday = Workout_HANDLER.preproc(tmp)
                    st.dataframe(CardioWorkout.head(10))

                elif data_file.name == 'RestingHeartRate.csv':
                    tmp = RHR_HANDLER.load_from_csv(df)

                elif data_file.name == 'StepCount.csv':
                    tmp = StepCount_HANDLER.load_from_csv(df)

                elif data_file.name == 'HeartRate.csv':
                    tmp = HeartRate_HANDLER.load_from_csv(df)

                else:
                    tmp = None


            else:
                st.write("not an valid file name")


