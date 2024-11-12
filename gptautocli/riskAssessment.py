import configparser
import os
import platform
from openai import OpenAI
from . import apiHandler

from .behaviorConfig import riskAssessmentPrompt

# Determine the appropriate config path based on the operating system
def get_config_path():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'gptautocli', 'config.ini')
    else:
        return os.path.expanduser('~/.gptautocli.config')

config_path = get_config_path()
config = configparser.ConfigParser()

class RiskAssessment:
    def __init__(self, user_interface, api_handler, risk_tolerance = -1):
        self.user_interface = user_interface
        self.api_handler = api_handler
        if risk_tolerance != -1:
            self.risk_tolerance = risk_tolerance
        else:
            self.risk_tolerance = int(self.get_risk_tolerance())
        self.api_handler = apiHandler.ApiHandler(user_interface)

    def assess_risk(self, command):
        if self.risk_tolerance == 6:
            return True
        else:
            # get the risk score 
            messages = [
                riskAssessmentPrompt,
                {
                    "role": "user", "content": command
                }
            ]
            response = self.api_handler.get_client().chat.completions.create(
                model='gpt-4o-mini',
                messages=messages,
            )

            # Get the response message
            response_message = response.choices[0].message.content
            risk_score = -1
            # get the highest integer in the response message
            for char in response_message:
                if char.isdigit() and int(char) > risk_score:
                    risk_score = int(char)
            # catch case where risk assessment AI does not return a risk score
            if risk_score == -1:
                risk_score = 3 # default to medium risk
            
            if risk_score < self.risk_tolerance:
                return True
            else:
                return self.user_interface.riskConfirmation(command, risk_score)
    def assess_overwrite_risk(self, filepath, content):
        if self.risk_tolerance == 6:
            return True
        else:
            risk_score = 4
            if risk_score < self.risk_tolerance:
                return True
            else:
                return self.user_interface.riskConfirmation("overwrite file at " + filepath + " with content: \n" + content, risk_score)
        
    def get_risk_tolerance(self):
        config.read(config_path)
        if 'command_risk' in config['DEFAULT']:
            return config['DEFAULT']['command_risk']
        else:
            return 0

    