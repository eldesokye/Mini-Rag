from .BaseController import BaseController
from .ProjectController import ProjectController
import os 
from langchain_community.document_loaders import PyMuPDFLoader , TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()  # call the constructor of the BaseController to load settings
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    
    def get_file_extension(self, file_id:str):
        file_extension = os.path.splitext(file_id)[-1]
        return file_extension
    
    def get_file_loader(self,file_id:str):
        file_extension = self.get_file_extension(file_id=file_id)
        file_path=os.path.join(self.project_path,file_id)

        if not os.path.exists(file_path):
            # raise ValueError(f"File not found: {file_path}")
            return None

        if file_extension in [ProcessingEnum.PDF.value, ProcessingEnum.TXT.value]:
            if file_extension == ProcessingEnum.PDF.value:
                return PyMuPDFLoader(file_path=file_path)
            else:
                return TextLoader(file_path=file_path,encoding='UTF-8')
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
    def get_file_content(self,file_id:str):
        try:
            loader = self.get_file_loader(file_id=file_id)
            if loader :
                documents = loader.load()
                return documents
            
            return None
        
        except Exception as e:
            raise ValueError(f"Error loading file content: {str(e)}")
        
    def process_file_content(self,file_content:list, file_id:str ,  chunk_size:int=1000, chunk_overlap:int=200):
        try:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap,length_function=len)
            file_content_texts = [
                rec.page_content for rec in file_content
            ]
            file_content_metadata=[
                rec.metadata for rec in file_content
            ]
            chunks = text_splitter.create_documents(file_content_texts,metadatas=file_content_metadata)

            return chunks
        
        except Exception as e:
            raise ValueError(f"Error processing file content: {str(e)}")

        



    