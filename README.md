# Project Overview

This project contains multiple Python scripts and other files that work together to form a terminal assistant called `singularity` (named for the fact that I used it to improve its own code).

## DISCLAIMER
This project has not been tested extensively and due to its nature, it is possible that it could cause harm to your system. AI models are not perfect and can make mistakes, and this project **GIVES AN AI MODEL THE ABILITY TO RUN ANY COMMAND ON YOUR SYSTEM** which while really cool could be argued to be a "really stupid and dangerous" idea. I suggest running this project in a virtual machine or on a system that you are willing to lose. I am not responsible for any damage that this project may cause to your system.  I personally have not run into any issues, but keep in mind that damage is possible.

### Capabilities

The terminal assistant is a powerful tool that can perform a variety of tasks, essesntially capable of anything that can be done in the terminal. Here is a small subset of its capabilities:
- **File Management**: Create, delete, and modify files and directories.
- **System Information**: Get information about the system, such as the operating system and hardware.
- **Write and Run Code**: Write and run code in multiple languages, including Python, Java, and C++.
- **Install Packages**: Install packages needed for development, such as `pip` and `npm`.
- **Fix Mistakes**: It is able to see command output and fix its own mistakes.
- **And Much More**: The assistant is capable of many other tasks, and can be easily extended to perform even more.

## Limitations
The assistant is not perfect, and there are some limitations to its capabilities. Here are a few of the limitations:
- **Prone to Mistakes**: Since the assistant is powered by OpenAI, it can sometimes make mistakes in its responses.
- **Limited access to up-to-date information**: The assistant may not have access to the most up-to-date information, as it is not connected to the intern
et.
- **Limited Ability to interact with commands that require user input**: The assistant is not yet able to interact with commands that require user input, 
- **Prone to Mistakes**: Since the assistant is powered by OpenAI, it can sometimes make mistakes in its responses.
- **Limited access to up-to-date information**: The assistant may not have access to the most up-to-date information, as it is not connected to the intern
et.
- **Limited Ability to interact with commands that require user input**: The assistant is not yet able to interact with commands that require user input, 
such as `sudo`, `nano`, or `vim`.  I am working on a solution to this.

### Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BSchoolland/terminal_assistant
    cd terminal_assistant
    ```

2. **Install Python** (if not already installed):
    - **For Linux**:
        ```bash
        sudo apt-get install python3 python3-pip
        ```
    - **For Mac**:
        ```bash
        brew install python3
        ```
    - **For Windows**:
        Download and install Python from [python.org](https://www.python.org/).

3. **Set up a Virtual Environment** (optional but recommended):
    ```bash
    ```
3. **Create a Branch**:
    ```bash
    git checkout -b your-feature-branch
    ```
4. **Make Your Changes**: Add your improvements or new features.
5. **Commit Your Changes**:
    ```bash
    git add .
    git commit -m "Description of your changes"
    ```
6. **Push to Your Fork**:
    ```bash
    git push origin your-feature-branch
    ```
7. **Open a Pull Request**: Click "New Pull Request" on the original repository.

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.