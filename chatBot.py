# manages chatbot state
import behaviorConfig

class ChatBot:
    def __init__(self, user_interface, api_handler, history):
        self.user_interface = user_interface
        self.api_handler = api_handler
        self.history = [ behaviorConfig.systemPrompt ] + history
        # get the client
        self.client = self.api_handler.get_client()
        # get the model
        self.model = self.user_interface.get_LLM_model()

        self.tools = behaviorConfig.tools
    
    def conversation_loop(self):
        while True:
            user_message = self.user_interface.get_user_input()


    
    def get_chat_history(self):
        return self.chat_history