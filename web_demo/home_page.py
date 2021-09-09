import streamlit as st
import os

import awesome_streamlit as ast
import cv2 #pip install opencv-python
def Home(conf):


    col1, col2 = st.beta_columns((1, 1))
    with col1:
        st.title("Main page here")

    with col2:
        st.title("how to use")
        # if os.path.exists(os.path.join(os.getcwd(), conf.path['image']['home']['apple_healthApp_data'])):
        #     image = cv2.imread(conf.path['image']['home']['apple_healthApp_data'])
        #     st.image(image, use_column_width=True, clamp=True)
        # else:
        #     st.error("image load failed")