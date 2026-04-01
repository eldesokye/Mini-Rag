from .BaseController import BaseController
from fastapi import UploadFile, File, HTTPException
from models import ResponseSignal
import os 

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()  # call the constructor of the BaseController to load settings


    def get_project_path(self, project_id:str):
        project_dir = os.path.join(self.file_dir, project_id)  # define the directory for the specific project
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)  # create the project directory if it doesn't exist

        return project_dir
    
    