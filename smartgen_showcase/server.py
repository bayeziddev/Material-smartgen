import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .core import SmartGenEngine

app = FastAPI(title="SmartGen Docs Upload Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOCS_DIR = Path(".")
ALLOWED_EXTENSIONS = {".md", ".markdown"}

@app.get("/", response_class=HTMLResponse)
async def upload_page():
    return """
    <!-- Upload interface HTML content remains the same -->
    <h1>Upload Manager</h1>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not any(file.filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Only .md and .markdown files are allowed")
    
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    file_path = DOCS_DIR / file.filename
    try:
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        return JSONResponse({"message": f"File {file.filename} uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@app.post("/rebuild")
async def rebuild_site():
    try:
        engine = SmartGenEngine("smartgen.yml", "site")
        engine.process_content_files()
        return JSONResponse({"message": "Site rebuilt successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rebuilding site: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)