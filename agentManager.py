# manages chatbot state

class AgentManager:
    def __init__(self, user_interface, conversation_agent, terminal_agent, history):
        self.user_interface = user_interface
        self.conversation_agent = conversation_agent
        self.terminal_agent = terminal_agent
        self.history = history
        self.chat_history = []
    
    def start_conversation(self):
        pass
    
    def get_chat_history(self):
        return self.chat_history