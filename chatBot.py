# manages chatbot state

class ChatBot:
    def __init__(self, user_interface, api_handler, history):
        self.user_interface = user_interface
        self.api_handler = api_handler
        self.history = history
        # get the client
        self.client = self.api_handler.get_client()
        # get the model
        self.model = self.user_interface.get_LLM_model()
        self.current_agent = self.conversation_agent
    
    def conversation_loop(self):
        while True:
            user_message = self.user_interface.get_user_message()


    
    def get_chat_history(self):
        return self.chat_history