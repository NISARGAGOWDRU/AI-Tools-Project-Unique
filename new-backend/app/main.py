import os
import logging
from uuid import uuid4
from dotenv import load_dotenv
import uvicorn
from pipeline.main import build_pipeline
from pipeline.state import PipelineState
from services.parse_and_save_docx import parse_and_save_docx

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  handlers=[
    logging.StreamHandler()
  ]
)

load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

pipeline = None

@app.on_event("startup")
async def startup_event():
    global pipeline
    pipeline = await build_pipeline()
    logging.info("Pipeline built and ready.")

@app.get("/")
def read_root():
    return {"message": "Vakils AI Backend is running"}

@app.post("/run_pipeline")
async def run_pipeline(payload: dict):
    """
    Run the LangGraph pipeline with the given payload.
    """
    global pipeline
    if not pipeline:
        return {"error": "Pipeline not initialized."}
    
    user_input = payload.get("query", "")
    state: PipelineState = {"user_input": user_input, "tool_calls": [], "status": "started"}
    thread_id = payload.get("thread_id") or str(uuid4())

    result = await pipeline.ainvoke(state, config={"configurable": {"thread_id": thread_id}})
    return {"final_result": result}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True, log_level="info")

MCP_DATA_DIR = os.getenv("MCP_DATA_DIR", "/data")
DOCS_DIR = os.path.join(MCP_DATA_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

@app.post("/upload_docx")
async def upload_docx(file: UploadFile = File(...)):
    """
    Endpoint to upload a DocX file and save it to the /data/docs directory.
    """
    if not file.filename or not file.filename.endswith(".docx"):
        return {"error": "Only .docx files are allowed."}
    
    save_path = os.path.join(DOCS_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    parse_and_save_docx(save_path)
    
    return {"uri": f"fs://docs/{file.filename}", "message": "File uploaded successfully."}