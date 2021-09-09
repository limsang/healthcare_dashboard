import streamlit as st
import os

import awesome_streamlit as ast
import cv2 #pip install opencv-python
def Notice(conf):

    st.title("얼마나 흘렸는지 분석해보자")
    st.markdown("***")

    col1, col2 = st.beta_columns((1, 1))
    with col1:
        st.title("What It's all about...")
        st.write(
            """
            1. 아이폰의 건강앱 & 애플워치 건강기록을 다운로드하여 스펙, 운동기록에 대한 분석결과를 조회할 수 있다.
            2. 기록 다운로드 방법은 오른편의 [Apple 공식 홈페이지 가이드](https://support.apple.com/ko-kr/guide/iphone/iph27f6325b2/ios)를 참고
            3. 유산소 이동 구글맵 활용 소스는 다음 [Github](https://github.com/nithishr/streamlit-data-viz-demo)를 참고
            
            
            ## How To use
            1. export.xml 파일을 업로드한다.
            2. 분석 탭으로 이동하여 운동기록을 선택 (csv 파일형식으로 변환됨)
            
            
             ## 그냥 봐  
            """
        )
        ast.shared.components.video_youtube(
            src=conf.path['links']['youtube_main']
        )

    with col2:
        st.title("Apple guide")

        if os.path.exists(os.path.join(os.getcwd(), 'images', 'apple_healthApp_data_down_1.png')):
            image = cv2.imread( conf.path['image']['home']['apple_healthApp_data'])
            st.image(image, use_column_width=True, clamp=True)
        else:
            st.subheader("image load failed")

        st.success(conf.path['email']['limsang'])