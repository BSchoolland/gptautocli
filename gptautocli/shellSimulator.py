import os
import subprocess
import select
import time
import sys
import selectors

import sys
from . import behaviorConfig

if behaviorConfig.get_os_type() == "Windows":
    import msvcrt  # Only import msvcrt if running on Windows

# parent class for all operating systems
class ShellSession:
    def __init__(self, userInterface=None):
        self.userInterface = userInterface
        self.command_counter = 0
    # same for all operating systems
    def is_command_allowed(self, command):
        # list of disallowed commands: nano, vi, vim FIXME: add windows and mac commands
        disallowed_commands = ["nano", "vi", "vim"]
        for disallowed_command in disallowed_commands:
            if command.startswith(disallowed_command):
                return f"TERMINAL ERROR: Command '{disallowed_command}' is not allowed. Please try using an alternative command ex: 'echo instead of nano'."
        # make sure the command does not include ``` bash or ```shell
        return "Yes"
    
    # to be implemented by the child classes
    def run_command(self, command, dangerouslyDisplayFullOutput=False):
        pass
    def close(self):
        pass
    def getCurrentDirectory(self):
        pass

class LinuxOrMacShellSession(ShellSession):
    def __init__(self, userInterface=None):
        super().__init__(userInterface)
        import pty
        master, slave = pty.openpty()
        self.process = subprocess.Popen(
            ['/bin/bash'],
            stdin=slave,
            stdout=slave,
            stderr=subprocess.STDOUT,
            close_fds=True,
            preexec_fn=os.setsid
        )
        self.master_fd = master
        os.close(slave)
    

    def run_command(self, command, dangerouslyDisplayFullOutput=False):
        # check if the command is allowed
        if self.is_command_allowed(command) != "Yes":
            return self.is_command_allowed(command)
            
        self.command_counter += 1  # Increment command counter
        end_tag = f"COMMAND_DONE_TAG{self.command_counter}"
        # Send command
        os.write(self.master_fd, (" " + command + "; echo " + end_tag + "\n").encode('utf-8'))
        Done = False
        first = True
        output = []

        while not Done:
            # Wait for input from either the process or stdin, with a timeout
            r, _, _ = select.select([self.master_fd, sys.stdin], [], [], 0.5)
            for ready_input in r:
                if ready_input == self.master_fd:
                    response = os.read(self.master_fd, 1024).decode('utf-8')
                    # Break the command up into lines
                    responses = response.split("\r\n")
                    for response in responses:
                        
                        if end_tag in response and command not in response:
                            # Command output finished
                            Done = True
                            break
                        if first:
                            # Skip the first line which is the prompt
                            first = False
                            continue
                        elif command + "; echo " + end_tag in response:
                            # Skip the command echo
                            continue
                        if self.userInterface:
                            self.userInterface.commandResult(response)
                        output.append(response)
                        

                elif ready_input == sys.stdin:
                    # Read from stdin (user input)
                    userInput = input() 
                    if userInput == "":
                        userInput = "\n" # if the user just presses enter, send a newline
                    if userInput == "exit" or userInput == "quit" or userInput == "q":
                        print("User interruption detected.")
                        Done = True
                        output.append("User ended the process. Exiting...")
                        # stop the process
                        os.write(self.master_fd, b"\x03")
                    else:
                        # write the input to the process
                        os.write(self.master_fd, (userInput + "\n").encode('utf-8'))

            # Check if the process has terminated
            if self.process.poll() is not None:
                break

        result = '\n'.join(output).strip()
        # limit the output to 1000 characters
        if len(result) > 1000 and not dangerouslyDisplayFullOutput:
            x = str(len(result) - 1000)
            result = result[:500] + "... " + x + " characters truncated to save tokens. ..." + result[-500:]
        return result

    def close(self):
        try:
            os.write(self.master_fd, b"exit\n")
            time.sleep(2)  # Give time for the exit command to process
        finally:
            os.close(self.master_fd)
            self.process.wait()
    def getCurrentDirectory(self):
        return self.run_command("pwd")


class WindowsShellSession(ShellSession):
    def __init__(self, userInterface=None):
        super().__init__(userInterface)
        # Create a persistent process that stays alive between commands
        self.process = subprocess.Popen(
            'cmd.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

    def run_command(self, command, dangerouslyDisplayFullOutput=False):
        # Check if the command is allowed
        command_status = self.is_command_allowed(command)
        if command_status != "Yes":
            return command_status

        self.command_counter += 1
        end_tag = f"COMMAND_DONE_TAG{self.command_counter}"
        
        # Send the command
        try:
            self.process.stdin.write(f"{command}\n")
            self.process.stdin.write(f"echo {end_tag}\n")
            self.process.stdin.flush()
        except IOError:
            return "Error: Failed to send command to process"

        output = []
        command_output_started = False
        Done = False

        while not Done:
            # Use a small timeout to avoid busy waiting
            try:
                line = self.process.stdout.readline()
                if not line:
                    Done = True
                    break
                    
                # Skip command echo and empty lines at the start
                if not command_output_started:
                    if command in line or not line.strip():
                        continue
                    command_output_started = True
                    
                if end_tag in line:
                    Done = True
                    break
                    
                if self.userInterface:
                    self.userInterface.commandResult(line.rstrip())
                output.append(line)

            except IOError:
                Done = True
                break

            # Check for user input (non-blocking)
            if msvcrt.kbhit():
                char = msvcrt.getwche()  # Use getwche for better Unicode support
                
                # Handle special cases
                if char == '\r':  # Enter key
                    print()  # New line after enter
                    self.process.stdin.write('\n')
                    self.process.stdin.flush()
                elif char == '\x03':  # Ctrl+C
                    print("^C")
                    self.process.stdin.write('\x03')
                    self.process.stdin.flush()
                    Done = True
                    output.append("User interrupted the process")
                elif char == '\x1a':  # Ctrl+Z
                    print("^Z")
                    self.process.stdin.write('\x1a')
                    self.process.stdin.flush()
                else:
                    # Send regular character input
                    try:
                        self.process.stdin.write(char)
                        self.process.stdin.flush()
                    except IOError:
                        Done = True
                        break

            # Check if process has terminated
            if self.process.poll() is not None:
                Done = True
                break

        result = ''.join(output).strip()
        # limit the output to 1000 characters
        if len(result) > 1000 and not dangerouslyDisplayFullOutput:
            x = str(len(result) - 1000)
            result = result[:500] + "... " + x + " characters truncated to save tokens. ..." + result[-500:]
        # Continue reading while the subprocess is running
        while True:
            line = self.process.stdout.readline()
            if not line:
                break  # No more output
            if end_tag in line:
                break  # Command output finished
            output.append(line)
        
        result = ''.join(output)
        
        return result

    def close(self):
        if self.process:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                time.sleep(1)  # Give time for the exit command to process
            except:
                pass  # Ignore errors during cleanup
            finally:
                self.process.terminate()
                self.process.wait()
    
    def getCurrentDirectory(self):
        return self.run_command("cd")




if __name__ == '__main__':
    print("<--BEGIN AUTOMATED TERMINAL SESSION-->")
    shell = LinuxOrMacShellSession()
    result = shell.run_command("ls -l")
    print("<--END AUTOMATED TERMINAL SESSION-->")
    print('the result is: ', result)
    shell.close()