from langgraph.checkpoint.memory import MemorySaver
from pipeline.state import PipelineState
from pipeline.agents.manager_agent import make_manager_agent
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from mcp_clients.client import get_resources
import logging

logger = logging.getLogger(__name__)

async def build_pipeline():
    graph = StateGraph(PipelineState)

    try:
        agent = await make_manager_agent()   # keep a single instance
        logger.info("Manager agent created successfully")
    except Exception as e:
        logger.error(f"Failed to create manager agent: {e}")
        raise

    # Fetch subpart summary URIs
    try:
        resources = await get_resources()
        # Handle Blob objects returned by MCP client
        subpart_summary_uris = []
        for r in resources:
            uri = str(getattr(r, 'metadata', {}).get('uri', ''))
            if 'subpart' in uri and uri.endswith('_summary.json'):
                subpart_summary_uris.append(uri)
        logger.info(f"Fetched {len(subpart_summary_uris)} subpart summary URIs")
    except Exception as e:
        logger.warning(f"Could not fetch subpart summary URIs: {e}")
        subpart_summary_uris = []

    async def manager_node(state: PipelineState) -> PipelineState:
        prompt = state.get("user_input", "")

        # Set subpart summary URIs in state
        state["subpart_summary_uris"] = subpart_summary_uris
        logger.info(f"Available subpart summary URIs: {subpart_summary_uris}")

        try:
            result = await agent.ainvoke({"messages": [HumanMessage(content=prompt)]})
            messages = result.get("messages", [])
            last_ai_message = next((m for m in reversed(messages) if isinstance(m, AIMessage)), None)
            output = last_ai_message.content if last_ai_message else ""
            if output is not None:
                state["last_tool_result"] = output
            state["status"] = "done"
        except Exception as e:
            logger.error(f"Error in manager node: {e}")
            state["last_tool_result"] = f"Error processing query: {str(e)}"
            state["status"] = "error"

        return state

    graph.add_node("manager", manager_node)
    graph.set_entry_point("manager")
    graph.add_edge("manager", END)
    
    return graph.compile(checkpointer=MemorySaver())