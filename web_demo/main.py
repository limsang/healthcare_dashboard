import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd
import numpy as np
from PyPDF2 import PdfFileReader
from home import Home
from analyzing_page import Dataset
from travel_viz import geo_workout


menu = ["홈", "분석", "About"]

def main():
	st.set_page_config(
		page_title="땀흘려",
		page_icon="🌍",
		layout="wide",
		initial_sidebar_state="expanded",
	)

	st.markdown("<h1 style='text-align: center; color: red;'>Apple Healthcare App</h1>", unsafe_allow_html=True)

	choice = st.sidebar.radio("Menu", menu) #) selectbox(

	if choice == "홈":
		Home()

	elif choice == "분석":
		Dataset()

	else:
		st.info("nothing")
		# geo_workout()

if __name__ == '__main__':

	main()