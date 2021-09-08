import json
import os

import streamlit as st
class conf(object):

    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, 'conf/conf.json')
        # print("config_path")
        with open(config_path) as json_file:
            self.path = json.load(json_file)