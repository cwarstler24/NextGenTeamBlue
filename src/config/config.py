import os
import configparser


class Config:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__),
                                   '../..', 'config.ini')

        self.config_file = configparser.ConfigParser()
        self.config_file.read(config_path)

    def getLogConfig(self):
        return self.config_file['log_config']

