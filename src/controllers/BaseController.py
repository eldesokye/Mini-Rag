from helpers.config import get_settings , settings
import os 
import random
import string


class BaseController:
    def __init__(self):
        self.app_settings = get_settings()  # load the settings when the controller is initialized

        self.base_dir = os.path.dirname(os.path.dirname(__file__))  # get the base directory of the project
        self.file_dir = os.path.join(self.base_dir, "assets/files")  # define the directory for storing uploaded files


    def generate_random_string(self, length:int = 12):
        """Generate a random string of fixed length."""
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(length)) 