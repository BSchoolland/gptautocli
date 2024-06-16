# Handles user input and provides output
import colorama
from colorama import Fore, Style
import os
from getTerminal import get_os_type

class UserInterface:
    def __init__(self):
        self.model = self.welcome()

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
        return model

    def choose_chat_history(self, history):
        pass

    def get_user_input(self):
        pass

    def get_LLM_model(self):
        return self.model