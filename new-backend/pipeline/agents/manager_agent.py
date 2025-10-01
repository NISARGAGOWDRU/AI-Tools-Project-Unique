from typing import Any
from langchain_core.runnables import Runnable
from langgraph.prebuilt import create_react_agent

from services.llm import make_llm
from mcp_clients.client import get_tools
import logging

logger = logging.getLogger(__name__)

async def make_manager_agent() -> Runnable:
    """
    Manager agent: orchestrates tool use by reasoning via the OSS LLM.
    Returns a LangChain Runnable that can be plugged into a LangGraph StateGraph.
    """
    llm = make_llm()
    
    # Get tools from MCP (will return empty list if MCP unavailable)
    tools = await get_tools()
    
    if not tools:
        logger.warning("No MCP tools available. Agent will run without tools.")
    else:
        logger.info(f"Loaded {len(tools)} tools from MCP server")
    
    agent = create_react_agent(
        model=llm,
        tools=tools,  # Can be empty list
        debug=True
    )

    return agent