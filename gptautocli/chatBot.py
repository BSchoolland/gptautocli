# manages chatbot state
import json


from . import behaviorConfig
from .shellSimulator import WindowsShellSession, LinuxOrMacShellSession

from . import overwriteFileFunction

class ChatBot:
    def __init__(self, user_interface, api_handler, riskAssessmentTool, model, history):
        self.user_interface = user_interface
        self.api_handler = api_handler
        self.conversation_history = [ behaviorConfig.systemPrompt ] + history
        # get the client
        self.client = self.api_handler.get_client()
        # get the model
        self.model = model

        self.tools = behaviorConfig.tools
        self.client = api_handler.get_client()
        self.model = user_interface.get_LLM_model()

        # fixme: get this from somewhere else
        osType = behaviorConfig.get_os_type()
        self.shell = WindowsShellSession(user_interface) if osType == "Windows" else LinuxOrMacShellSession(user_interface)
        self.riskAssessmentTool = riskAssessmentTool


    def conversation_loop(self):
        while True:
            user_message = self.user_interface.get_user_input()
            if user_message == "exit" or user_message == "quit" or user_message == "q":
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
                if self.user_interface.isInProgess():
                    self.user_interface.inProgressEnd()
            else:
                self.conversation_history.append({"role": "assistant", "content": response_message, "tool_calls": tool_calls})

            if not tool_calls:
                break
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    self.user_interface.inProgressStart(tool_call.function.name, tool_call.function.arguments)
                    if function_name == "run_command":
                        # Parse the JSON string into a dictionary
                        arguments = json.loads(tool_call.function.arguments)
                        command = arguments["command"]
                        dangerouslyDisplayFullOutput = arguments["dangerouslyDisplayFullOutput"] if "dangerouslyDisplayFullOutput" in arguments else False
                        self.user_interface.command(command)
                        function_result = ''
                        if (self.riskAssessmentTool.assess_risk(command)):
                            function_result = self.shell.run_command(command, dangerouslyDisplayFullOutput)
                        else:
                            function_result = "USER INTERRUPT: The user denied this command, ask them why and what they would prefer to do instead."
                        self.conversation_history.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "run_command",
                            "content": function_result
                        })
                    elif function_name == "overwrite_file":
                        # Parse the JSON string into a dictionary
                        arguments = json.loads(tool_call.function.arguments)
                        filepath = arguments["filepath"]
                        content = arguments["content"]
                        ## error handling
                        try:
                            if self.riskAssessmentTool.assess_overwrite_risk(filepath, content):
                                response_overwrite = overwriteFileFunction.write_content_to_file(filepath, content)
                            else:
                                response_overwrite = "USER INTERRUPT: The user denied this overwrite, ask them why and what they would prefer to do instead."
                            
                            self.conversation_history.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": "overwrite_file",
                                "content": response_overwrite
                            })
                        except ValueError as e:
                            self.conversation_history.append({
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": "overwrite_file",
                                "content": str(e)
                            })
                    
                    else:
                        self.conversation_history.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": "Tool not implemented"
                        })
        
        self.user_interface.chatBotMessage(response_message)
