from fastapi import FastAPI,APIRouter,Depends,UploadFile , status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,settings
from controllers import DataController
from controllers import ProjectController
import aiofiles
import logging

logger = logging.getLogger('uvicorn.error')
from models.enums.ResponseEnums import ResponseSignal

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,app_settings:settings = Depends(get_settings)):

    # validate the file properties 

    is_valid , result_signal = DataController().validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={"message": result_signal})
    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = DataController().generate_unique_filename(original_filename=file.filename, project_id=project_id)
    
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFULT_CHUNK_SIZE):  # read the file in chunks
                await f.write(chunk)  # write the chunk to the destination file
    except Exception as e:
        logger.error(f"Error occurred while uploading file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"message": f"{ResponseSignal.FILE_UPLOAD_FAILED.value}"}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_id": file_id}
    )