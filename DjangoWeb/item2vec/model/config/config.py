import json 
import os 
import sys

class config:
    def __init__(self):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, "config/dev_config.json")

        self.config = None 
        with open(config_path, 'r') as f:
            self.config = json.load(f)

    def get_config(self):
        return self.config        