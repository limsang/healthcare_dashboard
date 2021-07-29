import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd

from PyPDF2 import PdfFileReader
from home import Home
from analyzing_page import Dataset

menu = ["홈", "분석", "About"]

def main():
	st.set_page_config(layout="wide")
	st.markdown("<h1 style='text-align: center; color: red;'>Apple Healthcare App</h1>", unsafe_allow_html=True)

	choice = st.sidebar.radio("Menu", menu) #) selectbox(

	if choice == "홈":
		Home()

	elif choice == "분석":
		Dataset()

	else:
		st.subheader("About")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Jesse E.Agbe(JCharis)")

if __name__ == '__main__':

	main()