# Handles user input and provides output


from colorama import Fore, Style, init
import getpass
import os
from gptautocli.getTerminal import get_os_type

init() # ensure colorama works on windows
    
class UserInterface:
    def __init__(self):
        self.model = None
        self.inProgress = False

    def welcome(self, model, risk_tolerance):
        osType = get_os_type()

        # Disclaimer
        current_dir = os.getcwd()
        if risk_tolerance >= 6:
            risk_message = f"{Fore.RED}All commands will be executed without confirmation.{Style.RESET_ALL}"
        elif risk_tolerance <= 0:
            risk_message = f"{Fore.GREEN}All commands will require confirmation before execution.{Style.RESET_ALL}"
        else:
            risk_message = f"{Fore.YELLOW}Commands with a risk score above {risk_tolerance} will require confirmation before execution.{Style.RESET_ALL}"
        
        print(f"{Fore.CYAN}Welcome to gptautocli! {Style.RESET_ALL} \n  Using model: {model} \n  Current directory: {current_dir}\n  Detected OS: {osType}\n  {risk_message}")
        self.model = model
    
    def riskConfirmation(self, command, risk_score):
        choice = ''
        if risk_score >= 5:
            choice = input(Fore.MAGENTA + f"Risk score of {risk_score} detected for command: {command}.  Proceed? (y/n): " + Style.RESET_ALL)
        elif risk_score >= 4:
            choice = input(Fore.RED + f"Risk score of {risk_score} detected for command: {command}.  Proceed? (y/n): " + Style.RESET_ALL)
        elif risk_score == 1:
            choice = input(Fore.GREEN + f"Risk score of {risk_score} detected for command: {command}.  Proceed? (y/n): " + Style.RESET_ALL)
        else:
            choice = input(Fore.YELLOW + f"Risk score of {risk_score} detected for command: {command}.  Proceed? (y/n): " + Style.RESET_ALL)
        return choice.lower() == "y"

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

        print(Fore.GREEN + self.model + ": "+ Style.RESET_ALL + message)

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