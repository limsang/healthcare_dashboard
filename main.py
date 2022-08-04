import streamlit as st
from pages.home_page import Home
from pages.analyzing_page import Workout_Analysis
from pages.google_map_page import geo_workout
from pages.notice_page import Notice
from pages.judo_page import Judo

import sys
from conf.conf import conf as cf
from streamlit import cli as stcli

import logging
from logging.handlers import RotatingFileHandler

LOG_MAX_SIZE = 1024*1024*5 # 5MB
LOG_FILE_CNT = 3
LOG_LEVEL = logging.INFO

try:
    custom_logger = logging.getLogger(__name__)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    fileHandler = RotatingFileHandler("./logs/system.log", maxBytes=LOG_MAX_SIZE, backupCount=LOG_FILE_CNT)
    fileHandler.setFormatter(formatter)
    custom_logger.addHandler(fileHandler)
    custom_logger.setLevel(level=logging.INFO)

except Exception as e:
    print("error@ logger setting", e)

st.set_page_config(
		page_title="",
		page_icon="HealthCare",
		layout="wide",
		initial_sidebar_state="expanded",
	)


def main(custom_logger):

	"""
	set_page_config

	최상단에서 설정해주지않으면 커스텀 config 설정과 중복으로 인식해서 실행불가
	"""

	conf = cf()

	st.markdown("<h1 style='text-align: center; color: red;'> HealthCare </h1>", unsafe_allow_html=True)
	st.sidebar.header('main')

	menu = ["Home", "workouts", "cardios", 'judo_videos', 'about']
	choice = st.sidebar.radio("", menu)
	if choice == menu[0]:
		Home(conf, custom_logger)

	elif choice == menu[1]:
		Workout_Analysis(conf)

	elif choice == menu[2]:
		geo_workout(conf)

	elif choice == menu[3]:
		Judo(conf)

	else:
		Notice(conf)

if __name__ == '__main__':

	if st._is_running_with_streamlit:
		main(custom_logger)

	else:
		sys.argv = ["streamlit", "run", sys.argv[0], "--server.maxUploadSize=1028"]
		custom_logger.error(stcli.main())
		sys.exit(stcli.main())
