import streamlit as st
import pandas as pd

from utils.health_data_parser import HealthDataExtractor
from xml.etree import ElementTree as ET
from DFhandler.Workout import Workout

#
# VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
# 'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
# 'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
# 'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
#  'AppleStandTime.csv']

import os

def gen_file_path(dir):
    """
    상위경로에서 rawdata/~를 가져오도록
    """
    try:
        file_name = f"rawdata/{dir}.csv"
        res = os.path.join(os.path.abspath(""), file_name)
        return res

    except Exception as e:
        print("error at gen_file_path", e)
        return -1

def uploadXML_saveCSV():

    log_file_in_xml = st.sidebar.file_uploader("Upload XML", type=['xml'])

    if st.sidebar.button("xml데이터 저장"):
        if log_file_in_xml is not None:
            st.sidebar.info(log_file_in_xml)
            XML_PATH = '../rawdata/export.xml'
            """
            업로드한 파일을 지정된 경로로 복사한다.
            """
            if log_file_in_xml is not None:
                tree = ET.parse(log_file_in_xml)
                tree.write(XML_PATH)
                del tree

                data = HealthDataExtractor(XML_PATH)

                tag, fields, record_types = data.report_stats()
                tag += fields
                tag += record_types

                st.sidebar.info(tag)
                data.extract()

            else:
                st.sidebar.info("not an valid file")


def Workout_Analysis(conf):

    Workout_HANDLER = Workout()

    st.sidebar.title("XML 업로드")
    st.sidebar.info("추출한 XML 자료를 업로드한다")
    uploadXML_saveCSV()
    st.markdown("***")


    file = gen_file_path('Workout')
    if file != -1:
        df = pd.read_csv(file)
        WorkoutDF = Workout_HANDLER.load_from_csv(df)
        overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer,Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration = Workout_HANDLER.preproc(WorkoutDF)

        Workout_HANDLER.visualize(overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration)

    else:
        st.error("Workout을 진행하지 않았습니다..")



