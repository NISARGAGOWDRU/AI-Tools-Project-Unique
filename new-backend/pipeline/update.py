import asyncio
import logging
import json
from typing import Dict, Any, Optional, Set
from pipeline.state import PipelineState
from pipeline.messages import PipelineStatus, PROCESS_MESSAGES, SUCCESS_MESSAGES

logger = logging.getLogger(__name__)

class StatusUpdater:
    """Handles real-time status updates for the pipeline"""
    
    def __init__(self):
        self.update_callbacks = []
        self.sse_clients: Set[asyncio.Queue] = set()
    
    def add_callback(self, callback):
        """Add a callback function to receive updates"""
        self.update_callbacks.append(callback)
    
    def add_sse_client(self, queue: asyncio.Queue):
        """Register an SSE client queue for updates"""
        self.sse_clients.add(queue)
        logger.info(f"🦌 SSE client connected. Total clients: {len(self.sse_clients)}")
    
    def remove_sse_client(self, queue: asyncio.Queue):
        """Unregister an SSE client queue"""
        self.sse_clients.discard(queue)
        logger.info(f"🦌 SSE client disconnected. Total clients: {len(self.sse_clients)}")
    
    async def send_update(self, status: str, message: str, update_type: str = "update"):
        """Send status update to all registered callbacks and SSE clients"""
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
                logger.error(f"🦌 Error sending update to callback: {e}")
        
        # Send to all SSE clients
        disconnected_clients = []
        for client_queue in self.sse_clients:
            try:
                await client_queue.put(update_data)
            except Exception as e:
                logger.error(f"🦌 Error sending update to SSE client: {e}")
                disconnected_clients.append(client_queue)
        
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.remove_sse_client(client)

# Global status updater instance
status_updater = StatusUpdater()

async def update_status(state: PipelineState, status: str, message: str, update_type: str = "update"):
    """Update pipeline state status and send real-time update"""
    state["status"] = status
    await status_updater.send_update(status, message, update_type)
    logger.info(f"🦌 Pipeline status updated: {status}")

async def send_pipeline_update(state: PipelineState, status_key: str, custom_message: Optional[str] = None):
    """Send a pipeline status update with predefined or custom message"""
    message = custom_message or PROCESS_MESSAGES.get(status_key, "Processing...")
    update_type = "success" if status_key in SUCCESS_MESSAGES else "update"
    await update_status(state, status_key, message, update_type)