import subprocess
import threading
import queue
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your OpenAI API key from the environment variables
sudo_passwd = os.getenv("SUDO_PASSWD")


class ShellSession:
    def __init__(self):
        self.process = subprocess.Popen(
            ['/bin/bash'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            bufsize=1,
            universal_newlines=True
        )
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.stdout_thread = threading.Thread(target=self._enqueue_output, args=(self.process.stdout, self.stdout_queue))
        self.stderr_thread = threading.Thread(target=self._enqueue_output, args=(self.process.stderr, self.stderr_queue))
        self.stdout_thread.daemon = True
        self.stderr_thread.daemon = True
        self.stdout_thread.start()
        self.stderr_thread.start()

    def _enqueue_output(self, out, queue):
        for line in iter(out.readline, ''):
            queue.put(line)
        out.close()

    def get_prompt(self):
        # Retrieve the current username and hostname
        user = os.getenv("USER")
        hostname = os.getenv("HOSTNAME")
        # Run 'pwd' to get the current directory
        self.process.stdin.write('pwd\n')
        self.process.stdin.flush()
        current_dir = ''
        while True:
            line = self.stdout_queue.get(timeout=1)
            if line.strip() != '':
                current_dir = line.strip()
                break
        # Format similar to a typical bash prompt
        return f"{user}@{hostname}:{current_dir}$ "

    def run_command(self, command):
        prompt = self.get_prompt()
        # Print the prompt and the command
        print(prompt + command)
        # Send the command to the shell
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()
        
        # Read the output until we detect the next prompt
        output = []
        output.append(prompt + command)
        while True:
            try:
                line = self.stdout_queue.get(timeout=1)
                # Ignore the echo of the command
                if line.strip() == command:
                    continue
                # Assuming a prompt ends with '$ '
                if line.strip().endswith('$ '):
                    break
                if "password for" in line:
                    self.process.stdin.write(sudo_passwd + '\n')
                    self.process.stdin.flush()
                elif "Do you want to continue?" in line:
                    self.process.stdin.write('Y\n')
                    self.process.stdin.flush()
                print('line: ', line)
                output.append(line)
            except queue.Empty:
                break

        # Check for any errors
        # errors = []
        # while True:
        #     try:
        #         error_line = self.stderr_queue.get_nowait()
        #         errors.append(error_line)
        #     except queue.Empty:
        #         break
        # join the output into a single string
        string = ''
        for i in output:
            string += i
            string += '\n'
        # if errors:
        #     return ''.join(errors).join('\n')
        return string

    def close(self):
        # Close the process
        self.process.stdin.write('exit\n')
        self.process.stdin.flush()
        self.process.terminate()
        self.process.wait()

# Sample usage
if __name__ == '__main__':
    shell = ShellSession()
    print(shell.run_command('sudo apt-get install ruby'))
    shell.close()
