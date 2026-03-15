from fastapi import FastAPI,APIRouter
import os 
base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/welcome")
async def welcome():
    app_name = os.getenv("APP_NAME")
    app_version = os.getenv("APP_VERSION")
    
    return {"message": f"Welcome to {app_name} v{app_version}! This is a simple RAG application built with FastAPI."}
