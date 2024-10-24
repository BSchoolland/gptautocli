import configparser
import os
import platform
from openai import OpenAI

# Determine the appropriate config path based on the operating system
def get_config_path():
    return os.path.expanduser('~/.gptautocli.config')

config_path = get_config_path()
config = configparser.ConfigParser()

class ApiHandler:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.client = OpenAI(api_key=self.get_api_key())

    def get_client(self):
        return self.client
    
    def get_api_key(self):
        config.read(config_path)
        if 'openai_api_key' in config['DEFAULT']:
            return config['DEFAULT']['openai_api_key']
        else:
            self.user_interface.error("API key not found. Please run the setup process again.")
            exit(1)

    