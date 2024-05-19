import os
import pty
import subprocess
import select
import time
import getpass

# parent class for all opperating systems
class ShellSession:
    def __init__(self):
        self.command_counter = 0
    # same for all opperating systems
    def is_command_allowed(self, command):
        # list of disallowed commands: nano, vi, vim FIXME: add windows and mac commands
        disallowed_commands = ["nano", "vi", "vim"]
        for disallowed_command in disallowed_commands:
            if command.startswith(disallowed_command):
                return f"TERMINAL ERROR: Command '{disallowed_command}' is not allowed. Please try using an alternative command ex: 'echo instead of nano'."
        # make sure the command does not include ``` bash or ```shell
        if "```" in command:
            return "TERMINAL ERROR: More than just the command was entered. Please use 'command' and NOT ``` shell command ```."
        return "Yes"
    # to be implemented by the child classes
    def run_command(self, command):
        pass
    def close(self):
        pass

class LinuxOrMacShellSession(ShellSession):
    def __init__(self):
        super().__init__()
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
        end_tag = f"COMMAND_DONE_TAG{self.command_counter}"
        # Send command
        os.write(self.master_fd, (command + "; echo " + end_tag + "\n").encode('utf-8'))
        output = []

        # Continue reading while the subprocess is running
        first = True
        while True:
            r, _, _ = select.select([self.master_fd], [], [], 0.5)
            if r:
                response = os.read(self.master_fd, 1024).decode('utf-8')
                if first:
                    # Skip the first line which is the command echoed back
                    first = False
                    continue
                if "password for" in response:
                    # prompt the user for the password
                    password = getpass.getpass(prompt=response) + "\n"
                    os.write(self.master_fd, password.encode('utf-8'))
                    output.append(response)
                    continue
                elif end_tag in response and not "echo " + end_tag in response:
                    break
                
                if "Do you want to continue?" in response:
                    # send 'y' to continue
                    os.write(self.master_fd, b"y\n")

                elif "; echo " + end_tag in response:
                    response = response.replace("; echo " + end_tag, "")
                
               
                print(response, end='')
                output.append(response)
                # error handling
                # catch bash: error messages
                if "bash:" in response:
                    # send a command to the terminal to stop the current command
                    os.write(self.master_fd, b"\x03")
                    time.sleep(0.5) # give time for the terminal to process the command
                    # new line
                    os.write(self.master_fd, b"\n")
                    # a bit more time
                    time.sleep(0.5)
                    break
            # Check if the process has terminated
            if self.process.poll() is not None:
                break
        result = ''.join(output)
        # limit the output to 1000 characters
        if len(result) > 1000:
            print("Output too long. Truncating...")
            result = result[:500] + "... content truncated ..." + result[-500:]
        return result

    def close(self):
        try:
            os.write(self.master_fd, b"exit\n")
            time.sleep(2)  # Give time for the exit command to process
        finally:
            os.close(self.master_fd)
            self.process.wait()


class WindowsShellSession(ShellSession):
    def __init__(self):
        super().__init__()
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
            print(line, end='')  # Optionally print output in real-time
            output.append(line)
        
        result = ''.join(output)
        # limit the output to 1000 characters
        if len(result) > 1000:
            print("Output too long. Truncating...")
            result = result[:500] + "... content truncated ..." + result[-500:]
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
    shell = WindowsShellSession()
    result = shell.run_command("dir")
    shell.close()
    print("<--END AUTOMATED TERMINAL SESSION-->")
    print(result)
