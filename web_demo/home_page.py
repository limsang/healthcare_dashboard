import streamlit as st
import os

import awesome_streamlit as ast
import cv2 #pip install opencv-python
from DFhandler.BodySpec import BodySpec

BodyMass_dlr = "BodyMass"
V02Max_dlr = "VO2Max"
Height_dlr = "Height"
RestingHeartRate_dlr = "RestingHeartRate"
HeadphoneAudioExposure_dir = "HeadphoneAudioExposure"

def gen_file_path(dir):
    return os.path.join(os.getcwd(), dir)

def Home(conf):
    BodySpecHandler = BodySpec()

    """
    신체스펙을 생성하는 csv 파일들을 모두 전달한다.
    """
    csv_list = list()

    csv_list.append(BodyMass_dlr)
    csv_list.append(V02Max_dlr)
    csv_list.append(Height_dlr)
    csv_list.append(RestingHeartRate_dlr)
    csv_list.append(HeadphoneAudioExposure_dir)

    try:
        BodyMass, Height, V02Max, BasalEnergyBurned, HeadphoneAudioExposure, week_HeadphoneAudioExposure = BodySpecHandler.load_from_csv(csv_list)
        BodySpecHandler.visualize(BodyMass, Height, V02Max, BasalEnergyBurned, HeadphoneAudioExposure, week_HeadphoneAudioExposure)

    except Exception as e:
        st.error("XML파일 업로드 필요")


