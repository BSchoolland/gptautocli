# manages chatbot state

class AgentManager:
    def __init__(self, user_interface, conversation_agent, terminal_agent, api_handler, history):
        self.user_interface = user_interface
        self.conversation_agent = conversation_agent
        self.terminal_agent = terminal_agent
        self.api_handler = api_handler
        self.history = history
        # each entry will be in this format: (sender, message, action)   
        # sender can be "user", any agent name, or "system"
        # message is the text of the message
        # action is an optional field detailing any functions called by the agent and the parameters passed to them
        # get the client
        self.client = self.api_handler.get_client()
        # get the model
        self.model = self.user_interface.get_LLM_model()
        self.current_agent = self.conversation_agent
    
    def conversation_loop(self):
        while True:
            self.current_agent.step()

    
    def get_chat_history(self):
        return self.chat_history