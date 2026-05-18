import json
import sys
from typing import Any

from dejavu import Memory
from dejavu.local_config import DEFAULT_USER_ID, load_dejavu_config


TOOLS = [
    {
        "name": "memory_search",
        "description": "Search Deja Vu local memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "user_id": {"type": "string", "default": DEFAULT_USER_ID},
                "top_k": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    },
    {
        "name": "memory_add",
        "description": "Add messages to Deja Vu local memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "messages": {"type": "array", "items": {"type": "object"}},
                "user_id": {"type": "string", "default": DEFAULT_USER_ID},
            },
            "required": ["messages"],
        },
    },
    {
        "name": "memory_list",
        "description": "List Deja Vu local memories.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "default": DEFAULT_USER_ID},
                "limit": {"type": "integer", "default": 50},
            },
        },
    },
]


def _memory() -> Memory:
    return Memory.from_config(load_dejavu_config())


def _call_tool(name: str, arguments: dict[str, Any]) -> Any:
    memory = _memory()
    user_id = arguments.get("user_id", DEFAULT_USER_ID)
    if name == "memory_search":
        return {"results": memory.search(query=arguments["query"], user_id=user_id, limit=arguments.get("top_k", 5))}
    if name == "memory_add":
        return memory.add(arguments["messages"], user_id=user_id)
    if name == "memory_list":
        return memory.get_all(user_id=user_id, limit=arguments.get("limit", 50))
    raise ValueError(f"Unknown Deja Vu MCP tool: {name}")


def _respond(request: dict[str, Any], result: Any = None, error: Any = None) -> None:
    payload = {"jsonrpc": "2.0", "id": request.get("id")}
    if error is not None:
        payload["error"] = {"code": -32000, "message": str(error)}
    else:
        payload["result"] = result
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def run_stdio_mcp() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        request = json.loads(line)
        method = request.get("method")
        params = request.get("params") or {}
        try:
            if method == "initialize":
                _respond(request, {"protocolVersion": "2024-11-05", "serverInfo": {"name": "dejavu", "version": "0.1.0"}})
            elif method == "tools/list":
                _respond(request, {"tools": TOOLS})
            elif method == "tools/call":
                result = _call_tool(params["name"], params.get("arguments") or {})
                _respond(request, {"content": [{"type": "text", "text": json.dumps(result)}]})
            else:
                _respond(request, {})
        except Exception as exc:
            _respond(request, error=exc)
