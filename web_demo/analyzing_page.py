import streamlit as st
import pandas as pd

from utils.health_data_parser import HealthDataExtractor
from xml.etree import ElementTree as ET


from DFhandler.HeartRate import HeartRate
from DFhandler.Workout import Workout
from DFhandler.StepCount import StepCount
from DFhandler.RestingHeartRate import RestingHeartRate


VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
 'AppleStandTime.csv']


def uploadXML_saveCSV():
    log_file_in_xml = st.file_uploader("Upload XML", type=['xml'])
    if st.button("xml데이터 저장"):
        XML_PATH = 'data/export.xml'
        """
        업로드한 파일을 지정된 경로로 복사한다.
        """
        if log_file_in_xml is not None:
            tree = ET.parse(log_file_in_xml)
            tree.write(XML_PATH)
            del tree

            data = HealthDataExtractor(XML_PATH)
            data.report_stats()
            data.extract()

        else:
            st.info("not an valid file")

def Dataset():

    RHR_HANDLER = RestingHeartRate()
    Workout_HANDLER = Workout()
    StepCount_HANDLER = StepCount()
    HeartRate_HANDLER = HeartRate()

    tmp = None
    c = None
    st.title("XML 업로드")
    st.info("추출한 XML 자료를 업로드한다")
    uploadXML_saveCSV()
    st.markdown("***")

    st.title("그래프 조회")
    st.markdown("-> 조회하고자 하는 데이터셋을 업로드 하여 분석결과를 조회한다")
    data_file = st.file_uploader("Upload CSV", type=['csv'])

    if st.button("분석결과 조회"):
        if data_file is not None:
            if data_file.name in VALID_FILE_LIST:
                df = pd.read_csv(data_file)
                my_expander = st.beta_expander(label='csv details')

                with my_expander:
                    'Hello there!'
                    file_details = {"Filename": data_file.name, "FileType": data_file.type,"FileSize":data_file.size}
                    st.write(file_details)

                st.markdown("")
                st.markdown("")

                # 업로드한 파일명을 기준으로 분석
                if data_file.name == 'Workout.csv':
                    WorkoutDF = Workout_HANDLER.load_from_csv(df)
                    overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer,Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday = Workout_HANDLER.preproc(WorkoutDF)
                    Workout_HANDLER.visualize(overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday)

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
        else:
            st.info("should upload csv file first")
    st.markdown("***")

