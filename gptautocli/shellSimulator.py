import os
import subprocess
import select
import time
import sys

# parent class for all opperating systems
class ShellSession:
    def __init__(self, userInterface=None):
        self.userInterface = userInterface
        self.command_counter = 0
    # same for all opperating systems
    def is_command_allowed(self, command):
        # list of disallowed commands: nano, vi, vim FIXME: add windows and mac commands
        disallowed_commands = ["nano", "vi", "vim"]
        for disallowed_command in disallowed_commands:
            if command.startswith(disallowed_command):
                return f"TERMINAL ERROR: Command '{disallowed_command}' is not allowed. Please try using an alternative command ex: 'echo instead of nano'."
        # make sure the command does not include ``` bash or ```shell
        return "Yes"
    # to be implemented by the child classes
    def run_command(self, command):
        pass
    def close(self):
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
    

    def run_command(self, command):
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
        if len(result) > 1000:
            result = result[:500] + "... content truncated to save tokens. ..." + result[-500:]  # TODO: add a way to display the full output
        return result

    def close(self):
        try:
            os.write(self.master_fd, b"exit\n")
            time.sleep(2)  # Give time for the exit command to process
        finally:
            os.close(self.master_fd)
            self.process.wait()


class WindowsShellSession(ShellSession):
    def __init__(self, userInterface=None):
        super().__init__(userInterface)
        self.process = subprocess.Popen(
            'cmd.exe',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

    def run_command(self, command):
        # Check if the command is allowed
        command_status = self.is_command_allowed(command)
        if command_status != "Yes":
            return command_status
        
        end_tag = f"COMMAND_DONE_TAG{self.command_counter}"
        # Send command
        self.process.stdin.write(command + "\n")
        self.process.stdin.write(f"echo {end_tag}\n")
        self.process.stdin.flush()

        output = []
        # Continue reading while the subprocess is running
        while True:
            line = self.process.stdout.readline()
            if not line:
                break  # No more output
            if end_tag in line:
                break  # Command output finished
            output.append(line)
        
        result = ''.join(output)
        # limit the output to 1000 characters
        if len(result) > 1000:
            result = result[:500] + "... content truncated to save tokens. ..." + result[-500:] # TODO: add a way to display the full output
        return result

    def close(self):
        if self.process:
            self.process.stdin.write("exit\n")
            self.process.stdin.flush()
            time.sleep(1)  # Give time for the exit command to process
            self.process.terminate()
            self.process.wait()



if __name__ == '__main__':
    print("<--BEGIN AUTOMATED TERMINAL SESSION-->")
    shell = LinuxOrMacShellSession()
    result = shell.run_command("ls -l")
    print("<--END AUTOMATED TERMINAL SESSION-->")
    print('the result is: ', result)
    shell.close()