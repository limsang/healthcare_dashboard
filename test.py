import streamlit as st
from pages.test_page import Test

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

def main():
    """
	set_page_config

	최상단에서 설정해주지않으면 커스텀 config 설정과 중복으로 인식해서 실행불가
	"""

    conf = cf()
    st.markdown("<h1 style='text-align: center; color: red;'> HealthCare </h1>", unsafe_allow_html=True)
    st.sidebar.header('main')
    menu = ["Home", "workouts", "cardios", 'judo_videos', 'about']
    choice = st.sidebar.radio("", menu)
    Test(conf, custom_logger)
    # if choice == menu[0]:


    # else:
    #     Test(conf, custom_logger)

if __name__ == '__main__':
    # 여러번 call되는 함수 .. 왜?
    main()
