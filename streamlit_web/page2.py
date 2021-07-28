import streamlit as st
import pandas as pd


VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
 'AppleStandTime.csv']


def Dataset():
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV", type=['csv'])
    if st.button("Process"):
        if data_file is not None:
            if data_file.name in VALID_FILE_LIST:
                st.write("valid file name")
                file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
                st.write(file_details)
                df = pd.read_csv(data_file)
                st.dataframe(df.head(10))
            else:
                st.write("not an valid file name")
