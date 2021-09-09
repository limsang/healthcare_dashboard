import streamlit as st

import awesome_streamlit as ast

def Judo(conf):


    st.text_area('Area for textual entry')

    col1, col2 = st.beta_columns((1, 1))

    with col1:
        ast.shared.components.video_youtube(
            src=conf.path['links']['youtube_judo_1']
        )
        ast.shared.components.video_youtube(
            src=conf.path['links']['youtube_judo_2']
        )

    with col2:
        ast.shared.components.video_youtube(
            src=conf.path['links']['youtube_judo_3']
        )
        ast.shared.components.video_youtube(
            src=conf.path['links']['youtube_judo_4']
        )