from fastapi import FastAPI 

app = FastAPI(title="Mini-Rag", version="0.1.0", description="A simple RAG (Retrieval-Augmented Generation) application built with FastAPI.")

@app.get("/welcome")
def welcome_message():
    return {"message": "Welcome to Mini-Rag! This is a simple RAG application built with FastAPI."}