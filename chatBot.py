# manages chatbot state
import behaviorConfig
import json
from shellSimulator import WindowsShellSession, LinuxOrMacShellSession

class ChatBot:
    def __init__(self, user_interface, api_handler, history):
        self.user_interface = user_interface
        self.api_handler = api_handler
        self.conversation_history = [ behaviorConfig.systemPrompt ] + history
        # get the client
        self.client = self.api_handler.get_client()
        # get the model
        self.model = self.user_interface.get_LLM_model()

        self.tools = behaviorConfig.tools
        self.client = api_handler.get_client()
        self.model = user_interface.get_LLM_model()

        # fixme: get this from somewhere else
        osType = behaviorConfig.get_os_type()
        self.shell = WindowsShellSession() if osType == "Windows" else LinuxOrMacShellSession()


    def conversation_loop(self):
        while True:
            user_message = self.user_interface.get_user_input()
            if user_message == "exit":
                break
            self.get_gpt_response(user_message)

    def get_gpt_response(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        client = self.client
        while True:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.tools,
                tool_choice="auto"
            )

            # Get the response message
            response_message = response.choices[0].message.content
            if not response_message:
                response_message = ""
            tool_calls = response.choices[0].message.tool_calls
            if not tool_calls:
                self.conversation_history.append({"role": "assistant", "content": response_message})
            else:
                self.conversation_history.append({"role": "assistant", "content": response_message, "tool_calls": tool_calls})

            if not tool_calls:
                break
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    print(f"ChatGPT is calling the {function_name} function")
                    if function_name == "run_command":
                        # Parse the JSON string into a dictionary
                        arguments = json.loads(tool_call.function.arguments)
                        command = arguments["command"]
                        print('command:', command)
                        function_result = self.shell.run_command(command)
                        print('function_result:', function_result)
                        self.conversation_history.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "run_command",
                            "content": function_result
                        })
                    else:
                        self.conversation_history.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": "Tool not implemented"
                        })
        self.user_interface.info(f"AI: {response_message}")
        
    
    def get_chat_history(self):
        return self.chat_history