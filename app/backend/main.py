from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.backend.routes import router as item_router
import os

app = FastAPI()

# CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(item_router)

# Mount static files directory (adjust path as needed)
# app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")
app.mount("/", StaticFiles(directory="app/frontend/build", html=True), name="static")

# Serve index.html on root path
@app.get("/")
async def serve_index():
    index_path = os.path.join("app", "frontend", "build", "index.html")
    return FileResponse(index_path)
