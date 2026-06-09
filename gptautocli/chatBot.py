# manages chatbot state
import json

from . import behaviorConfig
from . import overwriteFileFunction
from .getTerminal import get_os_type
from .shellSimulator import WindowsShellSession, LinuxOrMacShellSession


class ChatBot:
    def __init__(self, user_interface, api_handler, riskAssessmentTool, model, history):
        self.user_interface = user_interface
        self.api_handler = api_handler
        self.conversation_history = [behaviorConfig.get_system_prompt()] + history
        self.client = api_handler.get_client()
        self.model = model
        self.tools = behaviorConfig.tools
        self.riskAssessmentTool = riskAssessmentTool

        osType = get_os_type()
        self.shell = WindowsShellSession(user_interface) if osType == "Windows" else LinuxOrMacShellSession(user_interface)

    def conversation_loop(self):
        while True:
            user_message = self.user_interface.get_user_input()
            if user_message in ("exit", "quit", "q"):
                break
            self.get_gpt_response(user_message)

    def get_gpt_response(self, prompt):
        self.conversation_history.append({"role": "user", "content": prompt})
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message.content or ""
            tool_calls = response.choices[0].message.tool_calls

            if not tool_calls:
                self.conversation_history.append({"role": "assistant", "content": response_message})
                if self.user_interface.is_in_progress():
                    self.user_interface.inProgressEnd()
                break

            self.conversation_history.append({"role": "assistant", "content": response_message, "tool_calls": tool_calls})
            for tool_call in tool_calls:
                self.user_interface.inProgressStart(tool_call.function.name, tool_call.function.arguments)
                result = self.run_tool_call(tool_call)
                self.conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": result
                })

        self.user_interface.chatBotMessage(response_message)

    def run_tool_call(self, tool_call):
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "run_command":
            command = arguments["command"]
            dangerouslyDisplayFullOutput = arguments.get("dangerouslyDisplayFullOutput", False)
            self.user_interface.command(command)
            if self.riskAssessmentTool.assess_risk(command):
                return self.shell.run_command(command, dangerouslyDisplayFullOutput)
            return "USER INTERRUPT: The user denied this command, ask them why and what they would prefer to do instead."

        if function_name == "overwrite_file":
            filepath = arguments["filepath"]
            content = arguments["content"]
            if self.riskAssessmentTool.assess_overwrite_risk(filepath, content):
                return overwriteFileFunction.write_content_to_file(filepath, content)
            return "USER INTERRUPT: The user denied this overwrite, ask them why and what they would prefer to do instead."

        return "Tool not implemented"
