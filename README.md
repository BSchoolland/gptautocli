# Project Overview

This project contains multiple Python scripts and other files that work together to form a terminal assistant called `gptautocli' powered by OpenAI's flagship GPT-4o model. The primary function of this package is to provide a conversational interface to the terminal, allowing users to run commands and perform tasks using natural language. 

## DISCLAIMER
This project has not been tested extensively and due to its nature, it is possible that it could cause harm to your system. AI models are not perfect and can make mistakes, and this project **GIVES AN AI MODEL THE ABILITY TO RUN ANY COMMAND ON YOUR SYSTEM** which has obvious risks. I strongly suggest not using this in a production environment, and cannot be held responsible for any damage caused by this project.


### Capabilities

This is a powerful tool that can perform a variety of tasks, essentially capable of anything that can be done in the terminal. Here is a small subset of its capabilities:
- **File Management**: Create, delete, and modify files and directories.
- **System Information**: Get information about the system, such as the operating system and hardware.
- **Write and Run Code**: Write and run code in most languages.
- **Install Packages**: Install packages needed for development through package managers like `pip` and `apt`.
- **Fix Mistakes**: It is able to see command output and will usually be able to fix mistakes that it makes.
- **And Much More**: I'm sure there are many more capabilities that I haven't thought of yet!

## Limitations
The assistant is not perfect, and there are some limitations to its capabilities. Here are a few of the limitations:
- **Prone to Mistakes**: Since the assistant is powered by OpenAI, it can sometimes make mistakes in its responses.
- **Limited access to up-to-date information**: The assistant may not have access to the most up-to-date information, as it is not connected to the internet.
- **Limited Ability to interact with commands that require user input**: The assistant has trouble interacting with commands that require user input, such as interactive programs or commands that require a password. 

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
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To use the terminal assistant:

1. **Start the Assistant**:
    ```bash
    python main.py
    ```

2. **Interact with the Assistant**:
    Follow the on-screen instructions to interact with the assistant.

---

### Contributing

I welcome contributions to this project! Please contact me (bschoolland@gmail.com) if you would like to contribute, or feel free to simply fork the repository and submit a pull request.

1. **Fork the Repository**: Click the "Fork" button on the top right of the repository page.
2. **Clone Your Fork**:
    ```bash
    git clone https://github.com/BSchoolland/gptautocli
    cd terminal_assistant
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

