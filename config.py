import json


class Config:
    def __init__(self, config_filename):
        with open(config_filename) as config_file:
            config = json.load(config_file)
        self.token = config['token']
