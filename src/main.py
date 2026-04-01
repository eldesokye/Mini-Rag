from fastapi import FastAPI 

from routes import base_router , data_router

from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import Settings,get_settings


app = FastAPI(title="Mini-Rag", version="0.1.0", description="A simple RAG (Retrieval-Augmented Generation) application built with FastAPI.")

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_conn = AsyncIOMotorClient(settings.MONOGODB_URI)
    app.db_client = app.mongodb_conn[settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_conn.close()



app.include_router(base_router)

app.include_router(data_router)



