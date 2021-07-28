import streamlit as st
import pandas as pd
import numpy as np
import os

st.title('Apple Healthcare Dashboard')
st.header("기록을 분석하자")

add_selectbox = st.sidebar.selectbox("Exercise", ("upper", "core", "bottom"))

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

st.text_input("기록을 분석하자")

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

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)

@st.cache
def load_data():
    data = pd.read_csv("BodyMass.csv")
    return data

# DF를 화면에 출력한다
# st.write("st.dataframe api")
# df = pd.DataFrame(np.random.randn(5, 2), columns=('col %d' % i for i in range(2)))
# st.dataframe(df.style.highlight_max(axis=0))
# st.write("st.table api")
# st.table(df)


checkbox_btn = st.checkbox('Checktbox Button')

if checkbox_btn:
    st.write('Great!')

data_load_state = st.text('Loading data...')
data = load_data()
st.table(data)
data_load_state.text("Done! (using st.cache)")

st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)