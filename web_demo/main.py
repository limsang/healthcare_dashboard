import streamlit as st
from home import Home
from analyzing_page import Dataset
from google_map import geo_workout

from conf.conf import conf as cf

from bodyspec import bodyspec

menu = ["Home", 'BodySpec', "gym", "outdoor", 'about']
def main():
	"""
	최상단에서 설정해주지않으면 커스텀 config 설정과 중복으로 인식해서 실행불가
	:return:
	"""
	st.set_page_config(
		page_title="땀흘려",
		page_icon="😎",
		layout="wide",
		initial_sidebar_state="expanded",
	)
	conf = cf()



	st.markdown("<h1 style='text-align: center; color: red;'>👑‍</h1>", unsafe_allow_html=True)

	choice = st.sidebar.radio("Menu", menu)

	if choice == menu[0]:
		Home(conf)

	elif choice == menu[1]:
		bodyspec(conf)

	elif choice == menu[2]:
		Dataset(conf)

	elif choice == menu[3]:
		geo_workout(conf)

	else:
		st.success(conf.path['email']['limsang'])

if __name__ == '__main__':
	main()