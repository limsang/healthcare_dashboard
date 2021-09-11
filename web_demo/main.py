import streamlit as st
from home_page import Home
from analyzing_page import Dataset
from google_map_page import geo_workout
from notice_page import Notice
from judo_page import Judo
import sys
from conf.conf import conf as cf
from bodyspec_page import bodyspec
from streamlit import cli as stcli
import subprocess
import os
def main():
	"""
	set_page_config

	최상단에서 설정해주지않으면 커스텀 config 설정과 중복으로 인식해서 실행불가
	"""
	st.set_page_config(
		page_title="",
		page_icon="HealthCare",
		layout="wide",
		initial_sidebar_state="expanded",
	)
	conf = cf()

	# st.balloons()

	st.markdown("<h1 style='text-align: center; color: red;'> HealthCare </h1>", unsafe_allow_html=True)
	st.sidebar.header('main')


	menu = ["Home", "workouts", "cardios", 'judo_videos', 'about']
	choice = st.sidebar.radio("", menu)

	if choice == menu[0]:
		Home(conf)

	elif choice == menu[1]:
		Dataset(conf)

	elif choice == menu[2]:
		geo_workout(conf)

	elif choice == menu[3]:
		Judo(conf)

	else:
		Notice(conf)



if __name__ == '__main__':
	if st._is_running_with_streamlit:
		main()
	else:
		sys.argv = ["streamlit", "run", sys.argv[0], "--server.maxUploadSize=1028"]
		sys.exit(stcli.main())
