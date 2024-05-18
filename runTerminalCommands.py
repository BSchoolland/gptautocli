import subprocess
import threading
import queue
import os
import time


class ShellSession:
    def __init__(self):
        self.process = subprocess.Popen(
            ['/bin/bash'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            bufsize=1,
            universal_newlines=True,
            env={"PS1": "$ "}
        )
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.stdout_thread = threading.Thread(target=self._enqueue_output, args=(self.process.stdout, self.stdout_queue))
        self.stderr_thread = threading.Thread(target=self._enqueue_output, args=(self.process.stderr, self.stderr_queue))
        self.stdout_thread.daemon = True
        self.stderr_thread.daemon = True
        self.stdout_thread.start()
        self.stderr_thread.start()
        self.command_counter = 0

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
        # Send the command to the shell but add a custom start and end token
        self.command_counter += 1
        print(command)
        self.process.stdin.write(command  + "; echo COMMAND_DONE_TAG" + str(self.command_counter) + '\n')
        self.process.stdin.flush()
        # wairt a short time to ensure some output is available
        # before we start reading it
        time.sleep(0.1)
        # Read the output until we detect the next prompt
        output = []
        output.append(prompt + command)
        while True:
            try:
                line = self.stdout_queue.get(timeout=3)
                
                # Ignore the echo of the command
                if line.strip() == command:
                    continue
                # Assuming a prompt ends with '$ '
                if line == 'COMMAND_DONE_TAG' + str(self.command_counter) + '\n':
                    print('command done!')
                    break
                print('line: ', line)                
                output.append(line)
            except queue.Empty:
                # FIXME: This is a hack to handle the case where we need to confirm a package installation
                # This assumes we've hit a confirmation prompt, although we have no way of knowing that yet as we don't have the line 
                self.process.stdin.write('Y\n')
                self.process.stdin.flush()
                
        string = ''
        for i in output:
            string += i
            string += '\n'
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
    print(shell.run_command('echo "hello world"'))
    # run a command that requires sudo
    print(shell.run_command('sudo npx create-react-app my-app'))

    shell.close()
