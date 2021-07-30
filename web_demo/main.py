import streamlit as st
from home import Home
from analyzing_page import Dataset
from google_map import geo_workout

menu = ["Home", "gym", "outdoor", 'about']
def main():

	st.set_page_config(
		page_title="땀흘려",
		page_icon="😎",
		layout="wide",
		initial_sidebar_state="expanded",
	)
	st.markdown("<h1 style='text-align: center; color: red;'>👑‍</h1>", unsafe_allow_html=True)

	choice = st.sidebar.radio("Menu", menu)

	if choice == menu[0]:
		Home()

	elif choice == menu[1]:
		Dataset()

	elif choice == menu[2]:
		geo_workout()

	else:
		st.success("lsh9225@naver.com")

if __name__ == '__main__':
	main()