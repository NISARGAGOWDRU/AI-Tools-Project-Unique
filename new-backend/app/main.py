# main.py
import os
import sys

# Add the project root directory to the Python path to resolve local imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import logging
import json
import re
import asyncio
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from pipeline.main import build_pipeline
from pipeline.state import PipelineState
from pipeline.update import status_updater, send_pipeline_update, PipelineStatus
from services.llm import make_llm
import json 

# Load env early
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("vakils_ai")


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
DOCS_DIR = MCP_DATA_DIR / "resources"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
pipeline = None


class PageDocument(BaseModel):
    html: Optional[str] = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RunPipelinePayload(BaseModel):
    documentId: Optional[str] = None
    pageNumber: Optional[int] = Field(default=1, alias="pageNumber")
    totalPages: Optional[int] = Field(default=None, alias="totalPages")
    document: Optional[PageDocument] = Field(default_factory=PageDocument)
    thread_id: Optional[str] = None
    query: Optional[str] = None
    triggerFromFrontend: Optional[bool] = False


@app.on_event("startup")
async def startup_event() -> None:
    global pipeline
    logger.info("Starting pipeline build...")
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
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error writing to file: {e}")
            raise

    await asyncio.to_thread(_sync_write)

async def _summarize_page(page_data: dict) -> str:
    """Summarize page content using LLM"""
    content = page_data.get("text", "").strip()
    if not content:
        html_content = page_data.get("html", "").strip()
        if html_content:
            import re
            content = re.sub(r'<[^>]+>', ' ', html_content)
            content = re.sub(r'\s+', ' ', content).strip()
    
    if not content:
        return "No content available to summarize."
    
    llm = make_llm()
    prompt = f"Please provide a concise summary of the following document content. Focus on the main points and key information:\n\nContent:\n{content}"
    response = await llm.ainvoke(prompt)
    return response.content

async def _create_document_summary(summaries: list, state: PipelineState = None) -> str:
    """Create overall document summary from page summaries"""
    if state:
        await send_pipeline_update(state, PipelineStatus.SUMMARIZING_PAGES)
    
    llm = make_llm()
    
    combined_summaries = "\n\n".join(summaries)
    max_chars = 3000 * 4  
    
    if len(combined_summaries) <= max_chars:
        prompt = f"Create a comprehensive document summary from these page summaries:\n\n{combined_summaries}"
        response = await llm.ainvoke(prompt)
        return response.content
    
    # If too long, process in chunks and combine
    logger.info("Processing summaries in chunks due to length")
    chunk_summaries = []
    chunk_size = max_chars // 2  
    
    current_chunk = []
    current_length = 0
    
    for summary in summaries:
        summary_length = len(summary) + 2  
        if current_length + summary_length > chunk_size and current_chunk:
            # Process current chunk
            chunk_text = "\n\n".join(current_chunk)
            prompt = f"Summarize these page summaries concisely:\n\n{chunk_text}"
            response = await llm.ainvoke(prompt)
            chunk_summaries.append(response.content)
            
            current_chunk = [summary]
            current_length = summary_length
        else:
            current_chunk.append(summary)
            current_length += summary_length
    
    # Process final chunk
    if current_chunk:
        chunk_text = "\n\n".join(current_chunk)
        prompt = f"Summarize these page summaries concisely:\n\n{chunk_text}"
        response = await llm.ainvoke(prompt)
        chunk_summaries.append(response.content)
    
    # Combine chunk summaries into final document summary
    final_combined = "\n\n".join(chunk_summaries)
    prompt = f"Create a comprehensive document summary from these section summaries:\n\n{final_combined}"
    response = await llm.ainvoke(prompt)
    return response.content

def _extract_compliance_for_frontend(pipeline_result: dict) -> dict:
    """Extract and format compliance results for frontend display"""
    try:
        logger.info("Extracting compliance data for frontend...")
        
        # Get final summary from ManagerAgent
        final_summary = pipeline_result.get('final_compliance_summary', {})
        if not final_summary:
            logger.warning("No 'final_compliance_summary' found in pipeline result.")
            return {
                "status": "analysis_incomplete",
                "message": "Final compliance summary was not generated."
            }

        # Extract only the final analysis from the ManagerAgent's summary
        frontend_data = {
            "status": "completed",
            "overall_score": final_summary.get('overall_compliance_score', 0),
            "compliance_status": final_summary.get('cfr21_status', 'Analysis Incomplete'),
            "satisfied_requirements": final_summary.get('satisfied_requirements', 'Not available'),
            "missing_requirements": final_summary.get('missing_requirements', 'Not available'),
            "recommendations": final_summary.get('recommendations', 'Not available'),
            "detailed_analysis": final_summary.get('detailed_analysis', 'Not available')
        }

        logger.info(f"🐼 Frontend compliance data prepared:\n{_safe_json_dumps(frontend_data)}")
        return frontend_data
        
    except Exception as e:
        logger.error(f"Error extracting compliance data for frontend: {e}")
        return {
            "status": "error",
            "message": f"Failed to extract compliance data: {str(e)}"
        }

def _safe_json_dumps(data: dict, indent: int = 2) -> str:
    """Safely dump a dictionary to a JSON string, handling non-serializable objects."""
    def default_serializer(o):
        if isinstance(o, (Path)):
            return str(o)
        try:
            # For LangChain messages or other complex objects
            if hasattr(o, 'dict'):
                return o.dict()
            return f"<<non-serializable: {type(o).__name__}>>"
        except Exception:
            return f"<<non-serializable: {type(o).__name__}>>"

    return json.dumps(data, indent=indent, default=default_serializer, ensure_ascii=False)


async def handle_detailed_check(query_data: dict, payload: RunPipelinePayload, state: dict) -> dict:
    """Handle detailed check requests for specific page and subpart"""
    state["detailed_check_active"] = True
    state["detailed_check_page"] = query_data.get('pages')
    state["detailed_check_subpart"] = query_data.get('subpart')
    
    await send_pipeline_update(state, PipelineStatus.STARTED)
    
    pass


@app.post("/run_pipeline")
async def run_pipeline(payload: RunPipelinePayload):
    """
    Accepts a payload with document page data, saves it to disk, and invokes the LangGraph pipeline.
    """
    global pipeline
    logger.info(f"Received payload: documentId=%s pageNumber=%s totalPages=%s", payload.documentId, payload.pageNumber, payload.totalPages)
    
    try:
        if payload.query:
            try:
                query_data = json.loads(payload.query)
                if query_data.get("action") == "detailed_check":
                    logger.info(f"🔍 DETAILED CHECK REQUEST DETECTED:")
                    logger.info(f"   - Page Number: {query_data.get('pages')}")
                    logger.info(f"   - Subpart: {query_data.get('subpart')}")
                    logger.info(f"   - Timestamp: {query_data.get('timestamp')}")
                    
                    state = {
                        "user_input": payload.query or "",
                        "tool_calls": [],
                        "status": PipelineStatus.STARTED,
                        "document_id": payload.documentId,
                    }
                    
                    return await handle_detailed_check(query_data, payload, state)
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logger.error(f"Error checking for detailed_check action: {e}")
    
    # Make documentId optional - use a default if not provided
    document_id = payload.documentId or "default_document"

    page_number = payload.pageNumber if payload.pageNumber and payload.pageNumber > 0 else 1

    document_folder_name = "document"
    uploaded_doc_folder_name = "uploaded_doc"
    document_dir = DOCS_DIR / document_folder_name / uploaded_doc_folder_name
    document_dir.mkdir(parents=True, exist_ok=True)
    
    # Create uploaded subfolder for page data
    uploaded_dir = document_dir / "uploaded"
    uploaded_dir.mkdir(parents=True, exist_ok=True)
    
    page_filename = f"page_{page_number}.json"
    page_path = uploaded_dir / page_filename

    page_data = {
        "html": payload.document.html or "",
        "metadata": payload.document.metadata or {},
    }

    try:
        await _write_json_file(page_path, page_data)
        logger.info("Saved page data to %s", page_path)
        
        summarized_dir = document_dir / "summarized"
        summarized_dir.mkdir(parents=True, exist_ok=True)
        
        summary_filename = f"page_{page_number}_summary.json"
        summary_path = summarized_dir / summary_filename
        
        page_summary = await _summarize_page(page_data)
        summary_data = {
            "page_number": page_number,
            "summary": page_summary,
            "original_page_path": str(page_path)
        }
        
        await _write_json_file(summary_path, summary_data)
        logger.info("Saved page summary to %s", summary_path)
        
        # Create embeddings directory and generate embeddings
        embeddings_dir = document_dir / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)
        
        from services.vector_embeddings import create_page_embeddings
        await create_page_embeddings(page_data, page_number, embeddings_dir)
        logger.info("Generated and saved embeddings for page %s", page_number)

    except Exception as exc:
        logger.exception("Failed to save page data or summary: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to save page data or summary")

    # Get all summarized page URIs
    summarized_dir = document_dir / "summarized"
    summarized_uris = []
    if summarized_dir.exists():
        summarized_uris = [str(p) for p in summarized_dir.glob("page_*_summary.json")]

    document_summary = None
    if payload.totalPages and page_number == payload.totalPages:
        try:
            summaries = []
            for uri in sorted(summarized_uris):
                with open(uri, 'r', encoding='utf-8') as f:
                    summary_data = json.load(f)
                    summaries.append(summary_data["summary"])

            if summaries:
                temp_state = {"status": "processing"}
                document_summary = await _create_document_summary(summaries, temp_state)
                logger.info("Created document summary")
                logger.info(f"Document Summary: {document_summary}")

                # Save document summary to file
                doc_summary_data = {
                    "document_id": payload.documentId,
                    "total_pages": payload.totalPages,
                    "document_summary": document_summary
                }
                doc_summary_path = document_dir / "document_summary.json"
                await _write_json_file(doc_summary_path, doc_summary_data)
                logger.info("Saved document summary to %s", doc_summary_path)
        except Exception as exc:
            logger.exception("Failed to create document summary: %s", exc)

    if not pipeline:
        logger.error("Pipeline not initialized.")
        raise HTTPException(status_code=503, detail="Pipeline not initialized")

    user_input = payload.query or ""
    
    state: PipelineState | dict = {
        "user_input": user_input,
        "tool_calls": [],
        "status": PipelineStatus.STARTED,
        "upload_completed": "false",
        "document_id": payload.documentId,
        "summarized_page_uris": summarized_uris,
        "document_summary": document_summary,
    }
    
    if document_summary:
        logger.info(f"Pipeline state updated with document_summary: {document_summary}")

    try:
        await _write_json_file(page_path, page_data)
        logger.info("Saved page data to %s", page_path)
        
        # Update page_urls with page URI
        state["page_urls"] = state.get("page_urls", {})
        state["page_urls"][payload.documentId] = state["page_urls"].get(payload.documentId, {})
        state["page_urls"][payload.documentId][payload.pageNumber] = str(page_path)

        if not pipeline:
            logger.error("Pipeline not initialized.")
            raise HTTPException(status_code=503, detail="Pipeline not initialized")

        thread_id = payload.thread_id or str(uuid4())
        logger.info("Invoking pipeline: thread_id=%s", thread_id)
        
        await send_pipeline_update(state, PipelineStatus.STARTED)

        result = await pipeline.ainvoke(state, config={"configurable": {"thread_id": thread_id}})

        if payload.totalPages is not None and payload.pageNumber == payload.totalPages:
            state["upload_completed"] = "true"
            logger.info("All pages uploaded. Setting upload_completed to True.")

    except Exception as exc:
        logger.exception("Failed to save page data or invoke pipeline: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to save page data or invoke pipeline")
    
    # Extract compliance results for frontend
    compliance_data = _extract_compliance_for_frontend(result)
    
    response_data = {
        "compliance_results": compliance_data,
        "document_summary": document_summary,
        "status": "completed"
    }
    logger.info(f"🐼 Data sent to frontend (final pipeline result):\n{_safe_json_dumps(response_data)}")
    return response_data

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True, log_level="info")
