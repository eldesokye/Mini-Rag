from .BaseController import BaseController
from fastapi import UploadFile, File, HTTPException
from models import ResponseSignal
from .ProjectController import ProjectController
import re 
import os 

class DataController(BaseController):
    def __init__(self):
        super().__init__()  # call the constructor of the BaseController to load settings
        self.size_scale = 1024 * 1024  # scale for converting MB to bytes


    def validate_uploaded_file(self , file:UploadFile ):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False , ResponseSignal.FILE_SIZE_EXCEEDS_LIMIT.value

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    

    def generate_unique_filename(self, original_filename:str,project_id:str):

        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_filename = self.get_clean_file_name(original_filename=original_filename)

        new_file_path = os.path.join(project_path, f"{random_filename}_{cleaned_filename}")

        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_filename}_{cleaned_filename}")

        return new_file_path , f"{random_filename}_{cleaned_filename}"

    def get_clean_file_name (self, original_filename:str):
        cleaned_file_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', original_filename)

        cleaned_file_name = cleaned_file_name.replace(' ', '_')

        return cleaned_file_name