from fastapi import FastAPI,APIRouter,Depends,UploadFile , status , Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,settings
from controllers import DataController
from controllers import ProjectController , ProcessController
import aiofiles
import logging
from .schemes.data import ProcessRequest
import asyncio
logger = logging.getLogger('uvicorn.error')
from models.enums.ResponseEnums import ResponseSignal
from models.ProjectModel import ProjectModel
from models.db_schemes import Project,DataChunk ,Asset
from models.ChunkModel import ChunkModel
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str,file:UploadFile,app_settings:settings = Depends(get_settings)):

    project_model = await ProjectModel.create_instace(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

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
    

    # store the Assets into the database

    asset_model = await AssetModel.create_instace(db_client=request.app.db_client)
    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type = AssetTypeEnum.FILE.value,
        asset_name = file_id,
        asset_size = os.path.getsize(file_path),

    )
    asset_record = await asset_model.create_asset(asset=asset_resource)



    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_id": str(asset_record.id),
                 "project_id": str(project.id)}
    )



@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str, process_request : ProcessRequest):
    # Here you would implement the logic to process the file based on the parameters in process_request
    # For example, you might call a method in DataController to handle the processing
    # You can access the parameters like this:
    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instace(db_client=request.app.db_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)


    asset_model = await AssetModel.create_instace(db_client=request.app.db_client)
    project_file_ids= {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(asset_prject_id=project.id, asset_name=process_request.file_id)
        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"signal": f"{ResponseSignal.NO_FILES_ERROR.value}"}
            )
        project_file_ids = {asset_record.id: asset_record.asset_name}

    else:
        
        project_files = await asset_model.get_all_project_assets(asset_project_id=project.id, asset_type=AssetTypeEnum.FILE.value)
        # project_files = await asyncio.gather(*project_files)
        project_file_ids = {
            record.id:record.asset_name
            for record in project_files
        }

        
    if len(project_file_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"message": f"{ResponseSignal.NO_FILES_ERROR.value}"}
        )


    process_controller = ProcessController(project_id=project_id)

    no_records = 0
    no_files = 0

    chunk_model = await ChunkModel.create_instace(db_client=request.app.db_client)


    if do_reset == 1 :
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)


    for asset_id , file_id in project_file_ids.items() if isinstance(project_file_ids, dict) else enumerate(project_file_ids):

        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"File content is empty or file not found for file_id: {file_id} in project_id: {project_id}")
            continue


        file_chunks = process_controller.process_file_content(file_content=file_content, file_id=file_id,
                                                            chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={"message": f"{ResponseSignal.FILE_PROCESSING_FAILED.value}"}
            )
        

        file_chunks_records = [
            DataChunk(
                project_id=project.id,
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=index + 1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id if isinstance(project_file_ids, dict) else None
            ) for index, chunk in enumerate(file_chunks)
        ]

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)

        no_files += 1




    return JSONResponse(
        content={"message": f"{ResponseSignal.FILE_PROCESSING_SUCCESS.value}",
                    "number_of_chunks": no_records,
                    "processed_files": no_files
                    },  
        status_code=status.HTTP_200_OK
    ) 
