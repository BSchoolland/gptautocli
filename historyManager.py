# class for saving and loading history to a json file
import json
import os

class HistoryManager:
    def __init__(self):
        self.avalible_chats = []

    def load_chat_history(self):
        if os.path.exists('history.json'):
            with open('history.json', 'r') as file:
                self.avalible_chats = json.load(file)
        else:
            self.avalible_chats = []
        return self.avalible_chats
    
    def save_chat_history(self, chat_history):
        self.avalible_chats.append(chat_history)
        with open('history.json', 'w') as file:
            json.dump(self.avalible_chats, file)
