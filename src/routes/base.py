from fastapi import FastAPI,APIRouter,Depends
import os 
from helpers.config import get_settings,settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/welcome")
async def welcome(app_settings:settings = Depends(get_settings)):
   # app_settings = settings()  # create an instance of the settings class to access the configuration values

    app_name = app_settings.APP_NAME  # access the APP_NAME from the settings
    app_version = app_settings.APP_VERSION  # access the APP_VERSION from the settings

    return {"message": f"Welcome to {app_name} v{app_version}! This is a simple RAG application built with FastAPI."}
