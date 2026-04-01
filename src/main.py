from fastapi import FastAPI 

from routes import base_router , data_router


app = FastAPI(title="Mini-Rag", version="0.1.0", description="A simple RAG (Retrieval-Augmented Generation) application built with FastAPI.")

app.include_router(base_router)

app.include_router(data_router)