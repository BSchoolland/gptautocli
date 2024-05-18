import sys
import subprocess
from getTerminal import get_terminal_type
import os
def is_inside_vscode():
    if os.getenv('TERM_PROGRAM') == 'vscode':
        return True
    return False

def run_in_new_terminal(command):
    terminal_type = get_terminal_type()

    if is_inside_vscode():
        # If inside VS Code, prompt the user
        run = input("Running in VS Code. The script will have to run in this terminal window (not the normal method). Continue? (y/n): ")
        if run.lower() in ['y', 'yes']:
            subprocess.run(['/bin/bash', '-c', command])
        else:
            print('To run normally, please run the script outside of VS Code.')
            return
    if terminal_type in ['gnome-terminal', 'konsole', 'xterm']:
        # Launch a new Linux terminal window
        subprocess.Popen([terminal_type, '--', '/bin/bash', '-c', command])
    elif terminal_type == 'cmd':
        # Launch a new command prompt in Windows
        subprocess.Popen(["start", "cmd", "/k", command], shell=True)
    elif terminal_type in ['iterm', 'mac_terminal']:
        # Launch a new terminal window in macOS
        subprocess.Popen(['open', '-a', terminal_type, '--args', '-e', command])
    else:
        raise Exception("Unsupported terminal or operating system.")

if __name__ == "__main__":
    script_name = "./ChatGPT.py"
    args = ' '.join(sys.argv[1:])  # All arguments except the script name itself
    command = f"python3 {script_name} {args}"
    run_in_new_terminal(command)
