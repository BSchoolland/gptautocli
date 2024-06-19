# sets up the openapi api and handles all the requests

import configparser
import os
from openai import OpenAI

# Get your OpenAI API key from the environment variables
config_path = os.path.expanduser('~/.terminal_assistant_config')
config = configparser.ConfigParser()

class ApiHandler:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.setup_api_key()
        self.client = OpenAI(api_key=self.get_api_key())
    def get_client(self):
        return self.client
    
    def get_api_key(self):
        if 'OpenAI_API_Key' in config['DEFAULT']:
            return config['DEFAULT']['OpenAI_API_Key']
        else:
            self.user_interface.error("API key not found. Please run the setup process again.")
            exit(1)

    def setup_api_key(self):
        """
        Setup the OpenAI API key
        """
        if not os.path.exists(config_path):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            api_key = self.user_interface.dialog("First time setup detected.  Welcome to the AI terminal assistant! Before we begin, we need to set up your OpenAI API key.  If you don't have an API key, follow the instructions at [FIXME: CREATE DOCUMENTATION] to get one. Please enter your OpenAI API key", secure=True)
 
            # confirm that the key works
            client = OpenAI(api_key=api_key)
            try:
                if self.test_client(client):
                    self.user_interface.info("API key verified successfully.")
                else:
                    self.user_interface.error("API key verification failed. Please check your API key and try again.")
                    exit(1)
            except Exception as e:
                self.user_interface.error("API key verification failed. Please check your API key and try again.")
                print(f"Error: {type(e).__name__}, {str(e)}")
                exit(1)

            config['DEFAULT'] = {'OpenAI_API_Key': api_key}
            with open(config_path, 'w') as configfile:
                config.write(configfile)
            self.user_interface.info("API key saved successfully.")
        else:
            config.read(config_path)

    def test_client(self, client):
        """
        Test the OpenAI API client by sending a simple prompt

        Parameters
        ----------
        client : OpenAI
            The OpenAI API client

        Returns
        -------
        bool
            True if the client is working, False otherwise
        """
        # Add user input to the conversation history
        conversation_history= [{"role": "user", "content": "Hi"}]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # Get the response message
        response_message = response.choices[0].message.content

        # Add the response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_message})

        if response_message:
            return True
        else:
            return False