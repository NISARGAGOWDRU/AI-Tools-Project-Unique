import os
from typing import List, Any, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient, Connection

MCP_URL = os.getenv("MCP_SERVER_URL", "")

def make_mcp_client() -> Optional[MultiServerMCPClient]:
    """
    Create a MultiServerMCPClient bound to the streamable HTTP MCP server.
    Returns None if MCP_SERVER_URL is not configured.
    """
    if not MCP_URL:
        return None

    config: dict[str, Connection] = {
        "mcp": {
            "transport": "streamable_http",
            "url": MCP_URL
        }
    }

    return MultiServerMCPClient(config)

async def get_tools() -> List[Any]:
    """
    List all tools registered in the MCP server.
    Returns empty list if MCP is not available.
    """
    client = make_mcp_client()
    if client is None:
        return []

    try:
        return await client.get_tools(server_name="mcp")
    except Exception as e:
        print(f"Warning: Could not connect to MCP server: {e}")
        return []

async def get_resources() -> List[dict]:
    """
    List all resources available in the MCP server.
    Returns empty list if MCP is not available.
    """
    client = make_mcp_client()
    if client is None:
        return []

    try:
        return await client.get_resources(server_name="mcp")
    except Exception as e:
        print(f"Warning: Could not connect to MCP server: {e}")
        return []