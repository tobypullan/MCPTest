from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from fastapi import FastAPI, Request

import os

# 1) Define the MCP server with a single tool
mcp = FastMCP("Example MCP Server")

@mcp.tool
def sum_two_numbers(a: float, b: float) -> float:
    """
    Return the sum of two numbers.
    Example call:
    {
      "name": "sum_two_numbers",
      "arguments": {"a": 2, "b": 3}
    }
    """
    return a + b

# 2) Turn the MCP server into an ASGI app and mount it on FastAPI
#    The `path` here is used for the MCP routing prefix (keep the trailing '/')
mcp_app = mcp.http_app(path="/mcp")

# Pass the MCP app's lifespan to FastAPI so startup/shutdown hooks run correctly
app = FastAPI(title="FastAPI + MCP", version="1.0.0", lifespan=mcp_app.lifespan)

# Mount the MCP routes at /mcp/
app.mount("/mcp", mcp_app)

# Optional: a simple health check / landing page
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "FastAPI app running. MCP endpoint at /mcp/ (POST JSON-RPC)."
    }

# 3) Local dev entrypoint (Render will use the start command you configure)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))  # Render supplies $PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
