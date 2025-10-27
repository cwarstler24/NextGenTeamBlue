import json
import os


class Config:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                   '../..', 'config.json')
        with open(config_path, encoding='utf-8') as f:
            self.config = json.load(f)

    def getLogConfig(self):
        return self.config['log_config']
