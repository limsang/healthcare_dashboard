import streamlit as st
from PIL import Image
import altair as alt
import pandas as pd
import numpy as np

import awesome_streamlit as ast
import cv2 #pip install opencv-python
def Home():

    # st.markdown("Streamlit is **_really_ cool**.")
    # expander = st.beta_expander("FAQ")
    #
    # expander.write("Here you could put in some really, really long explanations...")
    st.title("애플워치를 통해 기록한 기록정보를 분석")
    st.markdown("***")

    # hour_to_filter = st.slider('hour', 0, 23, 17)
    # st.subheader('Map of all pickups at %s:00' % hour_to_filter)

    col1, col2 = st.beta_columns((1, 1))
    with col1:
        st.title("What It's all about...")
        st.write(
            """
            1. 아이폰의 건강앱 & 애플워치 건강기록을 다운로드하여 스펙, 운동기록에 대한 분석결과를 조회할 수 있다.
            2. 기록 다운로드 방법은 오른편의 [Apple 공식 홈페이지 가이드](https://support.apple.com/ko-kr/guide/iphone/iph27f6325b2/ios)를 참고
            
            ## How To use
            1. export.xml 파일을 업로드한다.
            2. 분석 탭으로 이동하여 운동기록을 선택 (csv 파일형식으로 변환됨)
            
            
             ## 그냥 봐  
            """
        )
        ast.shared.components.video_youtube(
            src="https://www.youtube.com/embed/nSw96qUbK9o"
        )

    with col2:
        st.title("Apple guide")
        image = cv2.imread('images/apple_healthApp_data_down_1.png')
        st.image(image, use_column_width=True, clamp=True)