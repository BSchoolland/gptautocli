# gptautocli

This is the repository for the GPT Auto CLI project, a python package that provides a conversational interface to the terminal, allowing you to run commands and perform tasks using natural language.  

## DISCLAIMER
Despite its safety features, it is entirely possible that this package could cause harm to your system. AI models are not perfect and can make mistakes, and this project **GIVES AN AI MODEL THE ABILITY TO RUN ANY COMMAND ON YOUR SYSTEM** which can be dangerous. I am not responsible for any damage that may be caused by this project.

## Installation
**Warning: This package relies on the OpenAI API, which is a paid service.  You will need an API key and will be charged a small amount for usage.**

This package is available on PyPI, so you can install it using pip, assuming you have Python installed on your system.  If you don't have Python installed, you can download it from [python.org](https://www.python.org/).

To install the package, run the following command:
1. **Install the package**:
    ```bash
    pip install gptautocli
    ```
### First Run
When you first run `gptautocli`, you'll be prompted for an OpenAI API key:
- Create an account at [OpenAI](https://platform.openai.com/signup).
- Navigate to **Dashboard > API keys** and generate a new key.
- Paste the key into the prompt.

### Usage
To start the terminal assistant, simply run the following command:
```bash
gptautocli
```
You can then ask the assistant to perform any task you like, and it will respond with the appropriate command or set of commands to accomplish that task, whether it's creating a file, installing a package, or creating a Next.js project with 17 API routes and a database inside a Dockerized CI/CD Pipeline (okay maybe it can't do that last one but it would try).


## Capabilities
The terminal assistant is a powerful tool that can perform a variety of tasks, essentially capable of anything that can be done in the terminal. Here is a small subset of its capabilities:
- **File Management**: Create, delete, and modify files and directories.
- **System Information**: Get information about the system, such as the operating system and hardware.
- **Write and Run Code**: Write and run code in multiple languages, including Python, Java, and C++.
- **Install Packages**: Install packages needed for development, such as `pip` and `npm`.
- **Fix Mistakes**: It is able to see command output and fix its own mistakes.
- **And Much More**: The assistant is capable of many other tasks, and can be easily extended to perform even more.

## Limitations
The assistant is not perfect, and there are some limitations to its capabilities. Here are a few of the limitations:
- **Limited access to up-to-date information**: The assistant may not have access to the most up-to-date information, as it is not connected to the internet.
- **Limited Ability to interact with commands that require user input**: The assistant is not yet able to interact with commands that require user input, 
- **Prone to Mistakes**: Since the assistant is powered by OpenAI, it can sometimes make mistakes in its responses.
et.

## Safety Features
When you first set up this package, you'll be prompted to set a default risk tolerance level from 0 to 6.  Any command deemed by a secondary agent to be above this risk tolerance level will require user confirmation before being run.  If you wish to read every command before it is run, you can set the risk tolerance level to 0.  Setting a higher value will allow the assistant to run more commands without user confirmation.  I've also found that OpenAI's models are naturally quite cautious with the commands they generate, and will refuse to run dangerous commands even if explicitly asked to do so.

### How risk tolerance works
All commands are sent to gpt-4o-mini, a cheap but capable model, where it classifies the command without context to avoid bias. The model classifies commands based on the following scale:

1 - Read Only: Commands that simply read data without modifying anything at all
Example: ls -l - Lists files in a directory, changing nothing

2 - Safe: Commands that can write data but can not do any accidental damage
Example: touch myfile.txt - creates a file if it does not exist, but will not overwrite existing files

3 - Low Risk: Commands that alter files or locations, risky as it causes a change to the system.
Example: echo "text" >> myfile.txt - adds some data to the file

4 - High Risk: Commands that can modify data or cause other problems, leading to some data loss or serious inconvenience if used wrongly.
Example: rm myfile.txt - Deletes a file, leading to data loss if the wrong file is targeted

5 - Critical Risk (Accident-Prone): Commands that can cause severe damage or data loss if accidentally misused, often with no recovery option.
Example: rm -rf /Projects - Deletes all files in a likely important directory, leading to data loss

## Contributing

If you're interested in this project and would like to contribute, feel free to fork the repository and submit a pull request.

### Installation For Development 

If you just want to use the tool, please see the [Installation](#installation) section.  If you want to contribute to the project, follow these steps:

To set up the project in a development environment, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/BSchoolland/gptautocli
    cd gptautocli
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
    source venv/bin/activate
    ```

4. **Install the Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Install the project in editable mode**:
    ```bash
    pip install --editable .
    ```

6. **How I upload to PyPI**:
    ```bash
    python setup.py sdist bdist_wheel
    twine upload dist/*
    ```

From here, you can run the package as if you had installed it from pip normally, except that any changes you make to the code will be reflected in the package.


# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.