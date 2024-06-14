from openai import OpenAI
import os
from shellSimulator import LinuxOrMacShellSession, WindowsShellSession
import argparse
from getTerminal import get_terminal_type, get_os_type
import time
from colorama import init, Fore, Style
from getpass import getpass
import configparser

# better terminal output
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

# set a session
session = PromptSession(history=InMemoryHistory())

# Initialize colorama
init()



# Get your OpenAI API key from the environment variables
config_path = os.path.expanduser('~/.myappconfig')
config = configparser.ConfigParser()

def setup_api_key():
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        print("First time setup detected.")
        api_key = getpass("Please enter your OpenAI API key: ")
        config['DEFAULT'] = {'OpenAI_API_Key': api_key}
        with open(config_path, 'w') as configfile:
            config.write(configfile)
        print("API key saved successfully.")
    else:
        config.read(config_path)

def get_api_key():
    if 'OpenAI_API_Key' in config['DEFAULT']:
        return config['DEFAULT']['OpenAI_API_Key']
    else:
        print("API key not found. Please run the setup process again.")
        exit(1)

# Initial setup
setup_api_key()
api_key = get_api_key()

client = OpenAI(api_key=api_key)

# ANSI escape codes for styling
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"

MAX_HISTORY_LENGTH = 20 

# get os and terminal type
osType = get_os_type()
terminalType = get_terminal_type()
# Initialize the conversation history
conversation_history = [
    {"role": "system", "content": f"You are designed to work on OS: {osType} with terminal: {terminalType}.  You will be provided with terminal output at each step and will be expected to do nothing except provide the next command.  DO NOT PROVIDE ANY TEXT THAT IS NOT A COMMAND AS IT WILL BE ENTERED INTO THE TERMINAL AND MAY CAUSE ERRORS.  DO NOT SURROUND COMMANDS IN CODE BLOCKS AS THE ``` WILL BE ENTERED INTO THE COMMAND LINE AND CAUSE ERRORS. DO NOT TRY TO USE TOOLS LIKE NANO OR VI OR ACCESS ANY FORM OF GUI SINCE THESE WILL NOT FUNCTION CORRECTLY. You will only be able to enter commands. Once you have completed the goal or run into an unsolvable issue, type 'EXIT: (short description of what happened), success or failure' to end the program. Your goal is set by the user and is as follows: No goal defined, exit the program!"},
]

# Set a limit on the number of messages in the conversation history

def get_gpt_response(prompt, model="gpt-3.5-turbo"):
    # Add user input to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Trim the conversation history if it exceeds the maximum length
    if len(conversation_history) > MAX_HISTORY_LENGTH:
        conversation_history.pop(1)  # Remove the second element (index 1), keeping the system message

    response = client.chat.completions.create(
        model=model,
        messages=conversation_history
    )

    # Get the response message
    response_message = response.choices[0].message.content

    # Add the response to the conversation history
    conversation_history.append({"role": "assistant", "content": response_message})

    return response_message

def setGoal(goal):
    goal = f"<--BEGIN GOAL-->{goal}<--END GOAL-->"
    print(f"Goal set to: {goal}")
    osType = get_os_type()
    terminalType = get_terminal_type()
    if terminalType == "unknown":
        terminalType = "the default terminal for your OS"
    conversation_history[0]["content"] = f"You are designed to work on OS: {osType} with terminal: {terminalType}.  You will be provided with terminal output at each step and will be expected to do nothing except provide the next command.  DO NOT PROVIDE ANY TEXT THAT IS NOT A COMMAND AS IT WILL BE ENTERED INTO THE TERMINAL AND MAY CAUSE ERRORS.  DO NOT SURROUND COMMANDS IN CODE BLOCKS AS THE ``` WILL BE ENTERED INTO THE COMMAND LINE AND CAUSE ERRORS. DO NOT TRY TO USE TOOLS LIKE NANO OR VI OR ACCESS ANY FORM OF GUI SINCE THESE WILL NOT FUNCTION CORRECTLY. You will only be able to enter commands. Once you have completed the goal or run into an unsolvable issue, type 'EXIT: (short description of what happened), success or failure' to end the program. Your goal is set by the user and is as follows: " + goal
# main function for terminal mode
def terminalMode(goal, args):
    setGoal(goal)
    osType = get_os_type()
    # Create a shell session based on the OS type
    shell = WindowsShellSession() if osType == "Windows" else LinuxOrMacShellSession()
    # Run the terminal loop
    terminalLoop(args, shell)
    # close the program unless the user wants to chat
    chat = session.prompt("Press Enter to exit, or type a message to chat with the AI: ")
    if chat == "" or chat == "exit" or chat == "quit" or chat == "q":
        return
    else:
        chatMode(goal, args, initial_message=chat)

# A loop that allows the AI to interact with the terminal
def terminalLoop(args, shell, safe_mode=False):
    if osType == "Windows":
        shell_result = shell.run_command("dir")
    else:
        shell_result = shell.run_command("ls")
    while True:
        try:
            model = "gpt-4o" if args.s else "gpt-3.5-turbo"
            response = get_gpt_response(shell_result, model=model)

            if model == "gpt-3.5-turbo":
                print(Fore.YELLOW + Style.BRIGHT + model + Style.RESET_ALL + ": " + response)
            else:
                print(Fore.GREEN + Style.BRIGHT + model + Style.RESET_ALL + ": " + response)
            if response.startswith("EXIT:"):
                print("Program complete!")
                break
            # wait for the user to press enter before running the next command
            if safe_mode:
                input("Press Enter to continue...")
            # run the next command
            shell_result = ""
            try:
                shell_result = shell.run_command(response)
            except KeyboardInterrupt:
                # close the shell session, and make a new one
                print(f"{Fore.RED}{Style.BRIGHT}Current command stopped, press ctrl+c again quickly to exit the program.{Style.RESET_ALL}")
                shell.close()
                shell = WindowsShellSession() if osType == "Windows" else LinuxOrMacShellSession()
                shell_result = "Command interrupted by user, likely due to it getting stuck or taking too long."
                # wait 1 second to give the user a chance to exit the program
                time.sleep(1)               
                
                
            except Exception as e:
                print(e)
                shell_result = "Unknown error! Something may have gone wrong with the simulated terminal session! Automatically restarting the terminal session...  If this error persists, please exit the program"
                # close the shell session, and make a new one
                print(f"{Fore.RED}{Style.BRIGHT}Error occurred, restarting terminal session... If you want to exit the program, press ctrl+c{Style.RESET_ALL}")
                shell.close()
                shell = WindowsShellSession() if osType == "Windows" else LinuxOrMacShellSession()
                # wait 1 second to give the user a chance to exit the program
                
                time.sleep(1)
            
            
        except Exception as e:
            print(f"Error: {type(e).__name__}, {str(e)}")
            # exit the loop on error
            break

    
def chatMode(goal, args, initial_message=None):
    print(Fore.CYAN + Style.BRIGHT + "\n\nStarting chat session..." + Style.RESET_ALL)
    print("You can now chat with the AI. Type 'exit' to end the chat session, or ask the AI to do something else.")
    # update the system message to say that the program has ended and the GPT is allowed to talk normally
    conversation_history[0]["content"] = "Program complete, the goal was:" + goal + " Program complete. The goal was: install a package and run a script. You have been disconnected from the terminal and may now converse normally without worrying about errors. If you need to return to the terminal, you (the GPT) should simply respond with: `CONNECT TO TERMINAL: <task details>`. For example: `let's go back to the terminal and complete your new goal! CONNECT TO TERMINAL: install a package and run a script`"
    while True:
        try:
            if initial_message:
                user_input = initial_message
                initial_message = None
                print(f"{Fore.CYAN}{Style.BRIGHT}You: {Style.RESET_ALL}{user_input}")
            else:
                print(f"{Fore.CYAN}{Style.BRIGHT}You: {Style.RESET_ALL}", end="")
                user_input = session.prompt('')
                if user_input.lower() == "exit":
                    break
            model = "gpt-4o" if args.s else "gpt-3.5-turbo"
            response = get_gpt_response(user_input, model=model)
            if "CONNECT TO TERMINAL:" in response:
                message = response.split("CONNECT TO TERMINAL: ")[0]                
                goal = response.split("CONNECT TO TERMINAL: ")[1]
                if (not message == ""):
                    print(f"{Style.BRIGHT}{Fore.CYAN}AI: {Style.RESET_ALL}{message}")
                # goal = response.replace("CONNECT TO TERMINAL: ", "")
                print(f"{Style.BRIGHT}{Fore.CYAN}AI requested to connect to terminal with goal: {goal}{Style.RESET_ALL}")
                print((f"{Fore.WHITE}{Style.BRIGHT}Allow? (y/n): {Style.RESET_ALL}"), end="")
                answer = session.prompt('')
                if answer.lower() == "y":
                    terminalMode(goal, args)
                    break
                else:
                    print("AI access to terminal denied.")
            if model == "gpt-3.5-turbo":
                print(f"{Fore.YELLOW}{Style.BRIGHT}{model}: {Style.RESET_ALL}{response}")
            else:
                print(f"{Fore.GREEN}{Style.BRIGHT}{model}: {Style.RESET_ALL}{response}")
        except Exception as e:
            print(f"Error: {type(e).__name__}, {str(e)}")
            # exit the loop on error
            break

def introduction():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true", help="Use GPT-4o instead of GPT-3.5 Turbo (way smarter but more expensive)")
    args = parser.parse_args()

    model = "GPT-4o" if args.s else "GPT-3.5 Turbo"

    # Disclaimer
    
    current_dir = os.getcwd()
    print(f"{CYAN}{BOLD}Welcome to the AI terminal! {RESET} \n  Using model: {model} \n  Current directory: {current_dir}\n Detected OS: {osType}")
    try:
        print(Fore.RED + Style.BRIGHT + "Disclaimer: " + Style.RESET_ALL + Fore.YELLOW + "This program has not been extensively tested and is " + Style.BRIGHT + "NOT SAFE" + Style.RESET_ALL + Fore.YELLOW + " to use outside of a virtual machine or other isolated environment. ChatGPT is prone to mistakes, may misunderstand requests, and will be receiving " + Fore.RED + Style.BRIGHT + "FULL CONTROL" + Style.RESET_ALL + Fore.YELLOW + " of your terminal if you proceed. The developer of this program is not responsible for any damage caused by the use or misuse of this program.\n"  + "You can use Control-C to exit the program at any time, although the AI does type pretty fast..." + Style.RESET_ALL + "\n")
    except Exception as e:
        print(f"Error: {type(e).__name__}, {str(e)}")
    
    print(f"{Style.BRIGHT}Enter what you want the AI to do (q to cancel): {Style.RESET_ALL}")
    goal = session.prompt('> ')
    if goal == "" or goal == "exit" or goal == "quit" or goal == "q":
        # exit the program
        return
    return goal, args

if __name__ == "__main__":
    goal, args = introduction()
    if goal:
        terminalMode(goal, args)
    else:
        print("Cancelled. Exiting...")