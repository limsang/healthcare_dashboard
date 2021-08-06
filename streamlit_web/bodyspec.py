import streamlit as st

import os
from DFhandler.BodySpec import BodySpec
import awesome_streamlit as ast
import cv2 #pip install opencv-python

BodyMass_dlr = "BodyMass"
V02Max_dlr = "V02Max"
Height_dlr = "Height"
RestingHeartRate_dlr = "RestingHeartRate"
BasalEnergyBurned_dlr = "BasalEnergyBurned"

def gen_file_path(dir):
    return os.path.join(os.getcwd(), dir)

def bodyspec():

    BodySpecHandler = BodySpec()

    """
    신체스펙을 생성하는 csv 파일들을 모두 전달한다.
    """
    csv_list = list()

    csv_list.append(BodyMass_dlr)
    csv_list.append(V02Max_dlr)
    csv_list.append(Height_dlr)
    csv_list.append(RestingHeartRate_dlr)
    csv_list.append(BasalEnergyBurned_dlr)

    DF = BodySpecHandler.load_from_csv(csv_list)

    print("DF", DF)

    st.title("바디스펙")


    # Soccer_play_distance = alt.Chart(df).mark_area(
    #     color="lightblue",
    #     interpolate='step-after',
    #     line=True).encode(x='creationDate', y='value')
    #
    # st.altair_chart(Soccer_play_distance, use_container_width=True)

    # WorkoutDF = BodySpecHandler.load_from_csv(df)
    #
    # overall, weekdayCount, StrengthTraining, StrengthTraining_week, HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining, gymTrainingPerWeekday = Workout_HANDLER.preproc(
    #     WorkoutDF)
    # Workout_HANDLER.visualize(overall, weekdayCount, StrengthTraining, StrengthTraining_week,
    #                           HKWorkoutActivityTypeSoccer, Soccer_play_time, CardioWorkout, gymTraining,
    #                           gymTrainingPerWeekday)

