# sets up the openapi api and handles all the requests

class ApiHandler:
    def __init__(self, user_interface):
        self.user_interface = user_interface
        self.client = None

    def get_client(self):
        return self.client