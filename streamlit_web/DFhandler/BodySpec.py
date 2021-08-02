from DFhandler.handler_base import BaseHandler
import pandas as pd
from utils.utils import create_dataframe_with_initial_columns

import os
def gen_file_path(dir):
    file_name = f"data/{dir}.csv"
    return os.path.join(os.getcwd(), file_name)

class BodySpec(BaseHandler):

    def load_from_csv(self, csv_list):

        for csv in csv_list:
            if csv == "BodyMass":
                print(gen_file_path(csv))
            elif csv == "V02Max":
                print(gen_file_path(csv))

        # _df = create_dataframe_with_initial_columns(df)
        return "hellp"

    def preproc(self):
        pass

    def analysis_with_model(self):
        pass

    def visualize(self):
        pass