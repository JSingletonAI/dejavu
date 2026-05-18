import json
from typing import Optional

import typer
import uvicorn
from rich.console import Console

from dejavu import Memory
from dejavu.local_config import DEFAULT_USER_ID, config_path, load_dejavu_config, memory_db_path, write_default_config
from dejavu.mcp.server import run_stdio_mcp


app = typer.Typer(name="dejavu", help="Deja Vu private, local-first AI memory")
console = Console()


def _memory() -> Memory:
    return Memory.from_config(load_dejavu_config())


@app.command()
def init(force: bool = typer.Option(False, "--force", help="Overwrite existing config.")):
    """Create ~/.dejavu/config.json and ~/.dejavu/memories.db."""
    path = write_default_config(force=force)
    console.print("[green]Deja Vu initialized[/green]")
    console.print(f"Config: {path}")
    console.print(f"Memory DB: {memory_db_path()}")
    console.print("Set VENICE_API_KEY before running LLM-backed memory extraction.")
    console.print("Next: dejavu serve")


@app.command()
def add(text: str, user_id: str = typer.Option(DEFAULT_USER_ID, "--user-id")):
    """Add a memory for a local user."""
    result = _memory().add(text, user_id=user_id)
    console.print_json(data=result)


@app.command()
def search(query: str, user_id: str = typer.Option(DEFAULT_USER_ID, "--user-id"), top_k: int = typer.Option(5, "--top-k")):
    """Search local memory."""
    result = _memory().search(query=query, user_id=user_id, limit=top_k)
    console.print_json(data=result)


@app.command("list")
def list_memories(user_id: str = typer.Option(DEFAULT_USER_ID, "--user-id"), limit: int = typer.Option(50, "--limit")):
    """List local memories."""
    result = _memory().get_all(user_id=user_id, limit=limit)
    console.print_json(data=result)


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8765):
    """Run the local REST API."""
    uvicorn.run("dejavu.server.app:app", host=host, port=port)


@app.command()
def mcp():
    """Run the local stdio MCP server."""
    run_stdio_mcp()


@app.command()
def config():
    """Print the active config path and current foundation release config."""
    console.print(f"Config: {config_path()}")
    console.print(json.dumps(load_dejavu_config(), indent=2))
