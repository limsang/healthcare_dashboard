import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd

from PyPDF2 import PdfFileReader
from page1 import Home
from page2 import Dataset

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text


def main():
	st.title("File Upload Tutorial")

	menu = ["Home", "Dataset", "About"]
	choice = st.sidebar.selectbox("Menu", menu)

	if choice == "Home":
		Home()

	elif choice == "Dataset":
		Dataset()

	else:
		st.subheader("About")
		st.info("Built with Streamlit")
		st.info("Jesus Saves @JCharisTech")
		st.text("Jesse E.Agbe(JCharis)")


if __name__ == '__main__':
	main()