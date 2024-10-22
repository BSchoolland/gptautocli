# Handles user input and provides output


from colorama import Fore, Style
import getpass
import os
from gptautocli.getTerminal import get_os_type

    
class UserInterface:
    def __init__(self):
        self.model = None
        self.inProgress = False

    def welcome(self):
        osType = get_os_type()
        # choose a model
        print(f"{Style.BRIGHT}Choose a model to use: {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. gpt-4o-mini{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. gpt-4o{Style.RESET_ALL}")
        if input("Enter the number of the model you want to use: ") == "2":
            model = "gpt-4o"
        else:
            model = "gpt-4o-mini"
        # Disclaimer
        current_dir = os.getcwd()
        print(f"{Fore.CYAN}Welcome to the AI terminal! {Style.RESET_ALL} \n  Using model: {model} \n  Current directory: {current_dir}\n  Detected OS: {osType}")
        self.model = model

    def choose_chat_history(self, history):
        return []

    def get_user_input(self):
        input_text = input(Fore.CYAN + "You: " + Style.RESET_ALL)
        # make sure the input is not empty
        while not input_text:
            print(Fore.RED + "Please enter a message." + Style.RESET_ALL)
            input_text = input(Fore.CYAN + "You: " + Style.RESET_ALL)
        return input_text

    def get_LLM_model(self):
        return self.model
    
    def error(self, message):
        print(Fore.RED + message + Style.RESET_ALL)

    def info(self, message):
        print(Fore.CYAN + message + Style.RESET_ALL)

    def chatBotMessage(self, message):
        if self.model == "gpt-4o":
            print(Fore.GREEN + "ChatGPT-4o: " + Style.RESET_ALL + message)
        else:
            print(Fore.YELLOW + "ChatGPT-4o-mini: " + Style.RESET_ALL + message)

    def dialog(self, message, secure=False):
        if not secure:
            return input(message + ": ")
        else:
            # use getpass to hide the input
            return getpass.getpass(message + ": ")
        
    def isInProgess(self):
        return self.inProgress
    
    def inProgressStart(self, function_name, arguments):
        self.inProgress = True
        print(f"{Fore.YELLOW}AI entering the terminal.  Enter q to stop the process and return to the chat.{Style.RESET_ALL}")

    def inProgressEnd(self):
        self.inProgress = False
        print(f"{Fore.GREEN}Command completed.{Style.RESET_ALL}")

    def command(self, input):
        print('Command: ' + input)

    def commandResult(self, output):
        # if the otput ends with a newline, remove it
        if output.endswith("\n"):
            output = output[:-1]
        print(output)