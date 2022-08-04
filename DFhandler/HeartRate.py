from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns
import streamlit as st

class HeartRate(BaseHandler):

    @st.cache
    def load_from_csv(self,df):
        _df = create_dataframe_with_initial_columns(df)
        return _df

    def preproc(self):
        pass

    def analysis_with_model(self):
        pass
    def visualize(self):
        pass