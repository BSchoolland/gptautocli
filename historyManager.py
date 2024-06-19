# class for saving and loading history to a json file
import json
import os

class HistoryManager:
    def __init__(self):
        pass
        
    def load_chat_history(self):
        if os.path.exists('history.json'):
            with open('history.json', 'r') as file:
                return []
        else:
            return []
    
    def save_chat_history(self, chat_history):
        pass # FIXME: implement this
    
        # removed because tool calls cause errors when converting to json
        # with open('history.json', 'w') as file:
        #     json.dump(chat_history, file)
            
