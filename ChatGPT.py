from openai import OpenAI
import os
from dotenv import load_dotenv
from shellSimulator import ShellSession
import argparse

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit(1)

client = OpenAI(api_key=api_key)

# ANSI escape codes for styling
RESET = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"

MAX_HISTORY_LENGTH = 20 


# Initialize the conversation history
conversation_history = [
    {"role": "system", "content": "You are designed to work with the linux terminal.  You will be provided with terminal output at each step and will be expected to do nothing except provide the next command.  DO NOT PROVIDE ANY TEXT THAT IS NOT A COMMAND AS IT WILL BE ENTERED INTO THE TERMINAL AND MAY CAUSE ERRORS.  DO NOT SURROUND COMMANDS IN CODE BLOCKS AS THE ``` WILL BE ENTERED INTO THE COMMAND LINE AND CAUSE ERRORS. DO NOT TRY TO USE TOOLS LIKE NANO OR VI OR ACCESS ANY FORM OF GUI SINCE THESE WILL NOT FUNCTION CORRECTLY. You will only be able to enter commands. Once you have completed the goal or run into an unsolvable issue, type 'EXIT: (short description of what happened), success or failure' to end the program. Your goal is set by the user and is as follows: No goal defined, exit the program!"},
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
    conversation_history[0]["content"] = "You are designed to work with the linux terminal.  You will be provided with terminal output at each step and will be expected to do nothing except provide the next command.  DO NOT PROVIDE ANY TEXT THAT IS NOT A COMMAND AS IT WILL BE ENTERED INTO THE TERMINAL AND MAY CAUSE ERRORS.  DO NOT SURROUND COMMANDS IN CODE BLOCKS AS THE ``` WILL BE ENTERED INTO THE COMMAND LINE AND CAUSE ERRORS. DO NOT TRY TO USE TOOLS LIKE NANO OR VI OR ACCESS ANY FORM OF GUI SINCE THESE WILL NOT FUNCTION CORRECTLY. You will only be able to enter commands. Once you have completed the goal or run into an unsolvable issue, type 'EXIT: (short description of what happened), success or failure' to end the program. Your goal is set by the user and is as follows: " + goal
    
    

def terminalMode(goal, args):
    setGoal(goal)
    shell = ShellSession()
    shell_result = shell.run_command('ls')
    while True:
        try:
            model = "gpt-4o" if args.s else "gpt-3.5-turbo"
            response = get_gpt_response(shell_result, model=model)

            print(f"{model}: {response}")
            if response.startswith("EXIT:"):
                print("Program complete!")
                break
            # wait for the user to press enter before running the next command
            # input("Press Enter to continue...")
            # run the next command
            shell_result = ""
            try:
                shell_result = shell.run_command(response)
            except Exception as e:
                print(e)
                shell_result = "Unknown error! Something may have gone wrong with the simulated terminal session!"
            # print(shell_result)
            
        except Exception as e:
            print(f"Error: {type(e).__name__}, {str(e)}")
            # exit the loop on error
            break
    # close the program unless the user wants to chat
    chat = input("Press Enter to exit, or type a message to chat with the AI: ")
    if chat == "" or chat == "exit" or chat == "quit" or chat == "q":
        return
    else:
        chatMode(goal, args, initial_message=chat)
    
def chatMode(goal, args, initial_message=None):
    print(f"\n\n{BOLD}{CYAN}Starting chat session...{RESET}")
    print("You can now chat with the AI. Type 'exit' to end the chat session, or ask the AI to do something else.")
    # update the system message to say that the program has ended and the GPT is allowed to talk normally
    conversation_history[0]["content"] = "Program complete, the goal was:" + goal + " You have been disconnected from the terminal and may now talk normally without worrying about errors. If the user asks you to use the terminal again, respond with 'CONNECT TO TERMINAL: <new goal>'"
    while True:
        try:
            if initial_message:
                user_input = initial_message
                initial_message = None
                print(f"{BOLD}{CYAN}You: {RESET}{user_input}")
            else:
                user_input = input(f"{BLUE}{BOLD}You: {RESET}")
                if user_input.lower() == "exit":
                    break
            model = "gpt-4o" if args.s else "gpt-3.5-turbo"
            response = get_gpt_response(user_input, model=model)
            if response.startswith("CONNECT TO TERMINAL:"):
                goal = response.replace("CONNECT TO TERMINAL: ", "")
                print(f"{BOLD}{CYAN}AI requested to connect to terminal with goal: {goal}{RESET}")
                answer = input(f"{BOLD}Allow? (y/n): {RESET}")
                if answer.lower() == "y":
                    terminalMode(goal, args)
                    break
                else:
                    print("AI denied access to terminal.")
            if model == "gpt-3.5-turbo":
                print(f"{YELLOW}{BOLD}{model}: {RESET}{response}")
            else:
                print(f"{RED}{BOLD}{model}: {RESET}{response}")
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
    disclaimer = (
        f"{RED}{BOLD}Disclaimer:{RESET} {YELLOW}This program has not been extensively tested "
        f"and is {BOLD}NOT SAFE{RESET}{YELLOW} to use outside of a virtual machine or other isolated environment. "
        f"ChatGPT is prone to mistakes, may misunderstand requests, and will be receiving {RED}{BOLD}FULL CONTROL{RESET}{YELLOW} of your terminal if you proceed. "
        f"The developer of this program is not responsible for any damage caused by the use of this program.{RESET}\n"
    )
    current_dir = os.getcwd()
    print(f"{CYAN}{BOLD}Welcome to the AI terminal! {RESET} \n  Using: {model} model.\n  Current directory: {current_dir}\n")
    print(disclaimer)
    
    goal = input(f"{BOLD}Enter what you want the AI to do (q to cancel): {RESET}")
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