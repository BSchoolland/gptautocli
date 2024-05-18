import os
import pty
import subprocess
import select
import time
import getpass

class ShellSession:
    def __init__(self):
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
        self.command_counter = 0

        os.close(slave)

    def run_command(self, command):
        self.command_counter += 1
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
                # elif command + "; echo " + end_tag in response:
                #     # don't repeat the command
                #     continue
                elif "; echo " + end_tag in response:
                    response = response.replace("; echo " + end_tag, "")
                
                print(response, end='')
                output.append(response)
        return ''.join(output)

    def close(self):
        try:
            os.write(self.master_fd, b"exit\n")
            time.sleep(0.5)  # Give time for the exit command to process
        finally:
            os.close(self.master_fd)
            self.process.wait()

if __name__ == '__main__':
    print("<--BEGIN AUTOMATED TERMINAL SESSION-->")
    shell = ShellSession()
    # print(shell.run_command('echo "hello world"'))
    # sudo command:
    shell.run_command('sudo echo "hello world"')
    shell.close()
    print("<--END AUTOMATED TERMINAL SESSION-->")
