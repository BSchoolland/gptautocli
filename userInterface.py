# Handles user input and provides output


from colorama import Fore, Style
import getpass
import os
from getTerminal import get_os_type

class UserInterface:
    def __init__(self):
        self.model = None
        self.inProgress = False

    def welcome(self):
        osType = get_os_type()
        # choose a model
        print(f"{Style.BRIGHT}Choose a model to use: {Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. gpt-3.5-turbo{Style.RESET_ALL}")
        print(f"{Fore.GREEN}2. gpt-4o{Style.RESET_ALL}")
        if input("Enter the number of the model you want to use: ") == "2":
            model = "gpt-4o"
        else:
            model = "gpt-3.5-turbo"
        # Disclaimer
        current_dir = os.getcwd()
        print(f"{Fore.CYAN}Welcome to the AI terminal! {Style.RESET_ALL} \n  Using model: {model} \n  Current directory: {current_dir}\n  Detected OS: {osType}")
        try:
            print(Fore.RED + Style.BRIGHT + "Disclaimer: " + Style.RESET_ALL + Fore.YELLOW + "This program has not been extensively tested and is " + Style.BRIGHT + "NOT SAFE" + Style.RESET_ALL + Fore.YELLOW + " to use outside of a virtual machine or other isolated environment. ChatGPT is prone to mistakes, may misunderstand requests, and will be receiving " + Fore.RED + Style.BRIGHT + "FULL CONTROL" + Style.RESET_ALL + Fore.YELLOW + " of your terminal if you proceed. The developer of this program is not responsible for any damage caused by the use or misuse of this program.\n"  + "You can use Control-C to exit the program at any time, although the AI does type pretty fast..." + Style.RESET_ALL + "\n")
        except Exception as e:
            print(f"Error: {type(e).__name__}, {str(e)}")
        self.model = model

    def choose_chat_history(self, history):
        return []

    def get_user_input(self):
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
            print(Fore.YELLOW + "ChatGPT-3.5-turbo: " + Style.RESET_ALL + message)

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
        print(f"{Fore.YELLOW}Running {function_name} with arguments {arguments}...{Style.RESET_ALL}")

    def inProgressEnd(self):
        self.inProgress = False
        print(f"{Fore.GREEN}Command completed.{Style.RESET_ALL}")

    def command(self, input):
        print('Command: ' + input)

    def commandResult(self, output):
        print(output)