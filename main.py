# This is the entry point for the AI terminal assistant program.  It outlines the main program flow and calls other files at a high level.

# import modules
import apiHandler
import userInterface
import historyManager
import agentManager
import conversationAgent
import terminalAgent

if __name__ == '__main__':
    # initialize the UI
    user_interface = userInterface.UserInterface()
    # initialize the API handler
    api_handler = apiHandler.ApiHandler(user_interface)
    # initialize the conversation agent
    conversation_agent = conversationAgent.ConversationAgent()
    # initialize the terminal agent
    terminal_agent = terminalAgent.TerminalAgent()
    # initialize the history manager
    history_manager = historyManager.HistoryManager()
    
    # load chat history
    all_chat_history = history_manager.load_chat_history()
    
    # choose either a new chat or a previous chat
    history = user_interface.choose_chat_history(all_chat_history)
    
    # initialize the agent manager
    agent_manager = agentManager.AgentManager(user_interface, conversation_agent, terminal_agent, history, user_interface.get_LLM_model())
    
    # begin the conversation loop
    agent_manager.start_conversation()
    
    # once the conversation is over, save the chat history to a new file
    history_manager.save_chat_history(agent_manager.get_chat_history())
