import os
import subprocess
import select
import time
import sys
import getpass

from .getTerminal import get_os_type

if get_os_type() == "Windows":
    import msvcrt  # Only import msvcrt if running on Windows

OUTPUT_CHAR_LIMIT = 1000
DISALLOWED_COMMANDS = ["nano", "vi", "vim"]


def truncate_output(result, dangerouslyDisplayFullOutput=False):
    """Trim long command output to keep token usage down, keeping the head and tail."""
    if dangerouslyDisplayFullOutput or len(result) <= OUTPUT_CHAR_LIMIT:
        return result
    truncated = len(result) - OUTPUT_CHAR_LIMIT
    return f"{result[:500]}... {truncated} characters truncated to save tokens. ...{result[-500:]}"


# parent class for all operating systems
class ShellSession:
    def __init__(self, userInterface=None):
        self.userInterface = userInterface
        self.command_counter = 0

    # same for all operating systems: returns an error string if the command is
    # blocked, or None if it is allowed to run.
    def command_block_reason(self, command):
        for disallowed_command in DISALLOWED_COMMANDS:
            if command.startswith(disallowed_command):
                return f"TERMINAL ERROR: Command '{disallowed_command}' is not allowed. Please try using an alternative command ex: 'echo instead of nano'."
        return None

    # to be implemented by the child classes
    def run_command(self, command, dangerouslyDisplayFullOutput=False):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def getCurrentDirectory(self):
        raise NotImplementedError


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
        block_reason = self.command_block_reason(command)
        if block_reason:
            return block_reason

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

                    # Check if sudo is asking for password
                    if "[sudo] password for " in response or "Password:" in response:
                        password = getpass.getpass("")
                        os.write(self.master_fd, (password + "\n").encode('utf-8'))
                        continue

                    if end_tag in response and command not in response:
                        # Command output finished
                        Done = True
                        break
                    if first:
                        # Skip the first chunk which contains the prompt
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

        result = ''.join(output)  # Changed from '\n'.join to preserve all original formatting
        return truncate_output(result, dangerouslyDisplayFullOutput)

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
        block_reason = self.command_block_reason(command)
        if block_reason:
            return block_reason

        self.command_counter += 1
        end_tag = f"COMMAND_DONE_TAG{self.command_counter}"

        # Send the command
        self.process.stdin.write(f"{command}\n")
        self.process.stdin.write(f"echo {end_tag}\n")
        self.process.stdin.flush()

        output = []
        command_output_started = False
        Done = False

        while not Done:
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
                    self.process.stdin.write(char)
                    self.process.stdin.flush()

            # Check if process has terminated
            if self.process.poll() is not None:
                Done = True
                break

        result = ''.join(output).strip()
        return truncate_output(result, dangerouslyDisplayFullOutput)

    def close(self):
        if self.process:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                time.sleep(1)  # Give time for the exit command to process
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
