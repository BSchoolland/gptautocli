import sys
import subprocess
from getTerminal import get_terminal_type
import os
import argparse

def is_inside_vscode():
    # if os.getenv('TERM_PROGRAM') == 'vscode':
    #     return True
    return False

def run_in_new_terminal(command):
    terminal_type = get_terminal_type()

    if is_inside_vscode():
        # If inside VS Code, prompt the user
        run = input("Running in VS Code. The script will have to run in this terminal window (not the normal method). Continue? (y/n): ")
        if run.lower() in ['y', 'yes']:
            if terminal_type in ['gnome-terminal', 'konsole', 'xterm']:
                # run the command in the current terminal using bash
                subprocess.run(['/bin/bash', '-c', command])
            elif terminal_type == 'cmd':
                # run the command in the current terminal using cmd
                subprocess.run(['cmd', '/c', command])
            elif terminal_type in ['iterm', 'mac_terminal']:
                # run the command in the current terminal using iTerm
                subprocess.run(['open', '-a', terminal_type, '--args', '-e', command])
        else:
            print('To run normally, please run the script outside of VS Code.')
            return
    if terminal_type in ['gnome-terminal', 'konsole', 'xterm']:
        # Launch a new Linux terminal window
        subprocess.Popen([terminal_type, '--', '/bin/bash', '-c', command])
    elif terminal_type == 'cmd':
        # Launch a new command prompt in Windows
        subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    elif terminal_type in ['iterm', 'mac_terminal', 'zsh']:
        # Launch a new terminal window in macOS
        subprocess.Popen(['open', '-a', terminal_type, '--args', '-e', command])
    else:
        print("terminal type:", terminal_type, "os:", os.name)
        raise Exception("Unsupported terminal or operating system.")

if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action='store_true', help="Use the GPT-4o model instead of the GPT-3.5 Turbo model")
    # could potentially add these options in the future
    # parser.add_argument("-l", action='store_true', help="Long context mode, keeps conversation history for more than 20 messages")
    # parser.add_argument("-p", action='store_true', help="Persist the terminal session after the script ends")
    # if -h or --help is passed, print the help message and exit
    if "-h" in sys.argv or "--help" in sys.argv:
        parser.print_help()
        sys.exit(0)
    script_name = "/home/ben/personal/AI_Tasks/ChatGPT.py"
    args = ' '.join(sys.argv[1:])  # All arguments except the script name itself
    command = f"python3 {script_name} {args}"
    run_in_new_terminal(command)
