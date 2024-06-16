# manages chatbot state

class AgentManager:
    def __init__(self, user_interface, conversation_agent, terminal_agent, api_handler, history, model):
        self.user_interface = user_interface
        self.conversation_agent = conversation_agent
        self.terminal_agent = terminal_agent
        self.api_handler = api_handler
        self.history = history
        self.model = model
        self.chat_history = []
    
    def start_conversation(self):
        pass
    
    def get_chat_history(self):
        return self.chat_history