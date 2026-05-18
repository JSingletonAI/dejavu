from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from dejavu import Memory
from dejavu.local_config import DEFAULT_USER_ID, load_dejavu_config

app = FastAPI(title="Deja Vu", version="0.1.0")


class MemoryAddRequest(BaseModel):
    messages: list[dict[str, str]] | str
    user_id: str = DEFAULT_USER_ID


class SearchRequest(BaseModel):
    query: str
    user_id: str = DEFAULT_USER_ID
    top_k: int = Field(default=5, ge=1)


def get_memory() -> Memory:
    return Memory.from_config(load_dejavu_config())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "name": "dejavu"}


@app.post("/v1/memories")
def add_memory(payload: MemoryAddRequest) -> Any:
    return get_memory().add(payload.messages, user_id=payload.user_id)


@app.get("/v1/memories")
def list_memories(user_id: str = DEFAULT_USER_ID, limit: int = 50) -> Any:
    return get_memory().get_all(user_id=user_id, limit=limit)


@app.post("/v1/search")
def search_memory(payload: SearchRequest) -> Any:
    return get_memory().search(query=payload.query, user_id=payload.user_id, limit=payload.top_k)
