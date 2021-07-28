import streamlit as st
import streamlit.components.v1 as stc

# File Processing Pkgs
import pandas as pd

from PyPDF2 import PdfFileReader
from home import Home
from analyzing_page import Dataset

def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text


def main():

	st.title('Apple Healthcare Dashboard')
	hour_to_filter = st.slider('hour', 0, 23, 17)
	# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

	st.subheader('Map of all pickups at %s:00' % hour_to_filter)
	# 컬럼을 세로로 나누기
	# col1, col2, col3 = st.beta_columns(3)
	#
	#
	# with col1:
	#    st.header("A cat")
	#    st.image("https://static.streamlit.io/examples/cat.jpg", use_column_width=True)
	#
	# with col2:
	#    st.header("Button")
	#    if st.button("Button!!"):
	#        st.write("Yes")
	#
	# with col3:
	# 	st.header("Chart Data")
	# 	chart_data = pd.DataFrame(np.random.randn(50, 3), columns=["a", "b", "c"])
	# 	st.bar_chart(chart_data)


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