from fastapi import FastAPI 
from dotenv import load_dotenv
load_dotenv(".env")
from routes.base import base_router

app = FastAPI(title="Mini-Rag", version="0.1.0", description="A simple RAG (Retrieval-Augmented Generation) application built with FastAPI.")

app.include_router(base_router)