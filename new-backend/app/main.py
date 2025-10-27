# main.py
import os
import logging
import json
import asyncio
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# app-specific imports (assume these exist in your project)
from pipeline.main import build_pipeline
from pipeline.state import PipelineState  # keep if you use a class; otherwise treat as dict
# from services.parse_and_save_docx import parse_and_save_docx  # uncomment if used

# Load env early
load_dotenv()

# Logging
logger = logging.getLogger("vakils_ai")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(handler)

# FastAPI app
app = FastAPI(title="Vakils AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
MCP_DATA_DIR = Path(os.getenv("MCP_DATA_DIR", "/data"))
DOCS_DIR = MCP_DATA_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Pipeline placeholder (initialized on startup)
pipeline = None


class PageDocument(BaseModel):
    text: Optional[str] = ""
    html: Optional[str] = ""
    ooxml: Optional[str] = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RunPipelinePayload(BaseModel):
    documentId: str
    pageNumber: Optional[int] = Field(default=1, alias="pageNumber")
    document: Optional[PageDocument] = Field(default_factory=PageDocument)
    query: Optional[str] = ""
    thread_id: Optional[str] = None


@app.on_event("startup")
async def startup_event() -> None:
    global pipeline
    logger.info("Starting pipeline build...")
    # build_pipeline must be async - keep as you had
    pipeline = await build_pipeline()
    logger.info("Pipeline built and ready.")


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Vakils AI Backend is running"}


async def _write_json_file(path: Path, data: dict) -> None:
    """
    Write JSON to a file in a thread to avoid blocking the event loop.
    """
    def _sync_write():
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    await asyncio.to_thread(_sync_write)


@app.post("/run_pipeline")
async def run_pipeline(payload: RunPipelinePayload):
    """
    Accepts a payload with document page data, saves it to disk, and invokes the LangGraph pipeline.
    """
    logger.info("Received payload: documentId=%s pageNumber=%s", payload.documentId, payload.pageNumber)

    if not payload.documentId:
        logger.error("documentId is missing in payload")
        raise HTTPException(status_code=400, detail="documentId is required")

    page_number = payload.pageNumber if payload.pageNumber and payload.pageNumber > 0 else 1
    document_dir = DOCS_DIR / payload.documentId
    document_dir.mkdir(parents=True, exist_ok=True)
    page_filename = f"page_{page_number}.json"
    page_path = document_dir / page_filename

    page_data = {
        "text": payload.document.text or "",
        "html": payload.document.html or "",
        "ooxml": payload.document.ooxml or "",
        "metadata": payload.document.metadata or {},
        "query": payload.query or "",
    }

    try:
        await _write_json_file(page_path, page_data)
        logger.info("Saved page data to %s", page_path)
    except Exception as exc:
        logger.exception("Failed to save page data: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to save page data")

    global pipeline
    if not pipeline:
        logger.error("Pipeline not initialized.")
        raise HTTPException(status_code=503, detail="Pipeline not initialized")

    user_input = payload.query or ""
    # If PipelineState is a class, construct it appropriately. Here we use a plain dict if that's what your pipeline expects.
    state: PipelineState | dict = {
        "user_input": user_input,
        "tool_calls": [],
        "status": "started",
    }

    thread_id = payload.thread_id or str(uuid4())
    logger.info("Invoking pipeline: thread_id=%s", thread_id)

    try:
        # Keep the same invocation pattern you used previously
        result = await pipeline.ainvoke(state, config={"configurable": {"thread_id": thread_id}})
    except Exception as exc:
        logger.exception("Pipeline invocation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Pipeline invocation failed")

    return {"final_result": result}


if __name__ == "__main__":
    # Use 0.0.0.0 in containers; change as needed for local dev
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")

# TypeScript / Office.js reference — kept as comment for reference:
# /// <reference types="office-js" />
# declare const Word: any;
