
"""
csv 파일을 찾아 메뉴얼하게 업로드하는 로직.. 현재 사용 X
"""

import streamlit as st

VALID_FILE_LIST = ['HeartRate.csv', 'BodyMass.csv', 'Workout.csv', 'StepCount.csv', 'DistanceCycling.csv', 'WalkingAsymmetryPercentage.csv', 'DistanceWalkingRunning.csv',
'RestingHeartRate.csv', 'SixMinuteWalkTestDistance.csv', 'Height.csv', 'VO2Max.csv', 'HKDataTypeSleepDurationGoal.csv', 'HeartRateVariabilitySDNN.csv',
'WalkingSpeed.csv', 'AppleExerciseTime.csv', 'BasalEnergyBurned.csv', 'AppleStandHour.csv', 'WalkingHeartRateAverage.csv', 'WalkingStepLength.csv',
'ActiveEnergyBurned.csv', 'HeadphoneAudioExposure.csv', 'WalkingDoubleSupportPercentage.csv', 'FlightsClimbed.csv', 'SleepAnalysis.csv', 'ActivitySummary.csv',
 'AppleStandTime.csv']
#
# RHR_HANDLER = RestingHeartRate()
# Workout_HANDLER = Workout()
# StepCount_HANDLER = StepCount()
# HeartRate_HANDLER = HeartRate()
# data_file = st.file_uploader("Upload CSV", type=['csv'])
#     if st.button("분석결과 조회"):
#         if data_file is not None:
#             if data_file.name in conf.path['data']['VALID_FILE_LIST']:
#                 df = pd.read_csv(data_file)
#                 my_expander = st.beta_expander(label='csv details')
#
#                 with my_expander:
#                     file_details = {"Filename": data_file.name, "FileType": data_file.type,"FileSize":data_file.size}
#                     st.write(file_details)
#
#                 st.markdown("")
#                 st.markdown("")
#
#                 # 업로드한 파일명을 기준으로 분석
#                 if data_file.name == 'Workout.csv':
#                     WorkoutDF = Workout_HANDLER.load_from_csv(df)
#                     overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer,Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration = Workout_HANDLER.preproc(WorkoutDF)
#                     Workout_HANDLER.visualize(overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday, StrengthTraining_fft_duration)
#
#                 elif data_file.name == 'RestingHeartRate.csv':
#                     tmp = RHR_HANDLER.load_from_csv(df)
#
#                 elif data_file.name == 'StepCount.csv':
#                     tmp = StepCount_HANDLER.load_from_csv(df)
#
#                 elif data_file.name == 'HeartRate.csv':
#                     tmp = HeartRate_HANDLER.load_from_csv(df)
#
#                 else:
#                     tmp = None
#
#
#             else:
#                 st.write("not an valid file name")
#         else:
#             st.info("should upload csv file first")
#     st.markdown("***")