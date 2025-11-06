import asyncio
import logging
from typing import Dict, Any, Optional
from pipeline.state import PipelineState

logger = logging.getLogger(__name__)

class StatusUpdater:
    """Handles real-time status updates for the pipeline"""
    
    def __init__(self):
        self.update_callbacks = []
    
    def add_callback(self, callback):
        """Add a callback function to receive updates"""
        self.update_callbacks.append(callback)
    
    async def send_update(self, status: str, message: str, update_type: str = "update"):
        """Send status update to all registered callbacks"""
        logger.info(f"🦌 STATUS UPDATE: {status} - {message}")
        
        update_data = {
            "status": status,
            "message": message,
            "type": update_type,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Send to all callbacks
        for callback in self.update_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(update_data)
                else:
                    callback(update_data)
            except Exception as e:
                logger.error(f"🦌 Error sending update: {e}")

# Global status updater instance
status_updater = StatusUpdater()

async def update_status(state: PipelineState, status: str, message: str, update_type: str = "update"):
    """Update pipeline state status and send real-time update"""
    state["status"] = status
    await status_updater.send_update(status, message, update_type)
    logger.info(f"🦌 Pipeline status updated: {status}")

# Status constants for different pipeline stages
class PipelineStatus:
    STARTED = "started"
    SUMMARIZING_PAGES = "summarizing_pages"
    DOCUMENT_SUMMARIZED = "document_summarized"
    CONDUCTING_COMPLIANCE = "conducting_compliance"
    SUMMARIZING_COMPLIANCE = "summarizing_compliance"
    COMPLETED = "completed"
    ERROR = "error"

# Pre-defined status messages
STATUS_MESSAGES = {
    PipelineStatus.STARTED: "Initializing document processing...",
    PipelineStatus.SUMMARIZING_PAGES: "Summarizing document pages...",
    PipelineStatus.DOCUMENT_SUMMARIZED: "Document summary completed",
    PipelineStatus.CONDUCTING_COMPLIANCE: "Conducting CFR 21 compliance review...",
    PipelineStatus.SUMMARIZING_COMPLIANCE: "Generating final compliance summary...",
    PipelineStatus.COMPLETED: "Analysis complete",
    PipelineStatus.ERROR: "An error occurred during processing"
}

async def send_pipeline_update(state: PipelineState, status_key: str, custom_message: Optional[str] = None):
    """Send a pipeline status update with predefined or custom message"""
    message = custom_message or STATUS_MESSAGES.get(status_key, "Processing...")
    update_type = "message" if status_key == PipelineStatus.COMPLETED else "update"
    await update_status(state, status_key, message, update_type)