# This is the entry point for the AI terminal assistant program.  It outlines the main program flow and calls other files at a high level.

# import modules
import apiHandler
import userInterface
import historyManager
import chatBot

def main():
    # initialize the UI
    user_interface = userInterface.UserInterface()
    # initialize the API handler
    api_handler = apiHandler.ApiHandler(user_interface)
    # welcome the user
    user_interface.welcome()
    # initialize the history manager
    history_manager = historyManager.HistoryManager()
    
    # load chat history
    all_chat_history = history_manager.load_chat_history()
    
    # choose either a new chat or a previous chat
    history = user_interface.choose_chat_history(all_chat_history)
    
    # initialize the agent manager
    agent_manager = chatBot.ChatBot(user_interface, api_handler, history)

    # begin the conversation loop
    agent_manager.conversation_loop()
    # close the shell
    agent_manager.shell.close()
    # once the conversation is over, save the chat history to a new file
    history_manager.save_chat_history(agent_manager.conversation_history)


if __name__ == '__main__':
    try:
        # attempt to run the main program
        main()
    except Exception as e:
        print("An error occurred: ", e)
        input("Press enter to exit.")
    
