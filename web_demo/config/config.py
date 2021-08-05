import json

class Config(object):
    def __init__(self):

        with open('config.json', 'r') as f:
            self.config = json.load(f)