# Project Overview

This project contains multiple Python scripts and other files that work together to form a terminal assistant called `singularity`. Below is a comprehensive overview of each file in the project:

## Table of Contents

1. [apiHandler.py](#apiHandler.py)
2. [behaviorConfig.py](#behaviorConfig.py)
3. [chatBot.py](#chatBot.py)
4. [getTerminal.py](#getTerminal.py)
5. [history.json](#history.json)
6. [historyManager.py](#historyManager.py)
7. [LICENSE](#LICENSE)
8. [main.py](#main.py)
9. [print_name.py](#print_name.py)
10. [requirements.txt](#requirements.txt)
11. [shellSimulator.py](#shellSimulator.py)
12. [userInterface.py](#userInterface.py)


## Descriptions

### apiHandler.py
Sets up the OpenAI API and handles all requests. This script manages API keys and client interactions using the OpenAI service.

### behaviorConfig.py
Configures the system prompt and defines the behavior of the AI by providing context about the environment it operates in.

### chatBot.py
Manages the state of the chatbot, handles messages, and interacts with tools based on user commands.

### getTerminal.py
Detects the operating system and terminal type to tailor commands and interactions.

### history.json
Stores the chat history in a structured JSON format, which allows the assistant to maintain context across sessions.

### historyManager.py
Provides functionality to load and save chat history to a JSON file.

### LICENSE
Contains the MIT License under which the project is released.

### main.py
The entry point of the AI terminal assistant program. It initializes components and starts the conversation loop.

### print_name.py
A simple script that prints "Singularity" 50 times.

### requirements.txt
Lists the dependencies required to run the project.

### shellSimulator.py
Simulates terminal sessions for different operating systems, handling command execution and processing.

### userInterface.py
Handles user input and provides output in a user-friendly manner, incorporating various utilities to interact with the terminal.


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

---

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

We welcome contributions to this project! To contribute, follow these steps:

1. **Fork the Repository**: Click the "Fork" button on the top right of the repository page.
2. **Clone Your Fork**:
    ```bash
    git clone https://github.com/yourusername/terminal_assistant.git
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

