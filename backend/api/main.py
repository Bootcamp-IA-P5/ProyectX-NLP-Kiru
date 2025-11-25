# backend/api/main.py
from fastapi import FastAPI

app = FastAPI(
    title="YouTube Hate Speech Detector API",
    description="API para detectar mensajes de odio en comentarios de YouTube",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    """Endpoint de salud básico"""
    return {"status": "healthy", "service": "hate-speech-detector"}

@app.get("/")
async def root():
    return {"message": "API funcionando", "version": "0.1.0"}
