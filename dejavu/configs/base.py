import os
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from dejavu.configs.rerankers.config import RerankerConfig
from dejavu.embeddings.configs import EmbedderConfig
from dejavu.llms.configs import LlmConfig
from dejavu.vector_stores.configs import VectorStoreConfig

# Set up the directory path
home_dir = os.path.expanduser("~")
dejavu_dir = os.environ.get("DEJAVU_DIR") or os.path.join(home_dir, ".dejavu")


def maybe_migrate_legacy_dejavu_dir():
    legacy = os.path.expanduser("~/.dejavu/history.db")
    target = os.path.expanduser("~/.dejavu/memories.db")
    if os.path.exists(legacy) and not os.path.exists(target):
        return (
            "Legacy Dejavu data found at ~/.dejavu/history.db. "
            "Deja Vu will not import it automatically; copy it to "
            "~/.dejavu/memories.db manually if you trust the data."
        )
    return None


class MemoryItem(BaseModel):
    id: str = Field(..., description="The unique identifier for the text data")
    memory: str = Field(
        ..., description="The memory deduced from the text data"
    )  # TODO After prompt changes from platform, update this
    hash: Optional[str] = Field(None, description="The hash of the memory")
    # The metadata value can be anything and not just string. Fix it
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata for the text data")
    score: Optional[float] = Field(None, description="The score associated with the text data")
    created_at: Optional[str] = Field(None, description="The timestamp when the memory was created")
    updated_at: Optional[str] = Field(None, description="The timestamp when the memory was updated")


class MemoryConfig(BaseModel):
    vector_store: VectorStoreConfig = Field(
        description="Configuration for the vector store",
        default_factory=VectorStoreConfig,
    )
    llm: LlmConfig = Field(
        description="Configuration for the language model",
        default_factory=LlmConfig,
    )
    embedder: EmbedderConfig = Field(
        description="Configuration for the embedding model",
        default_factory=EmbedderConfig,
    )
    history_db_path: str = Field(
        description="Path to the local Deja Vu memory database",
        default=os.environ.get("DEJAVU_MEMORY_DB") or os.path.join(dejavu_dir, "memories.db"),
    )
    reranker: Optional[RerankerConfig] = Field(
        description="Configuration for the reranker",
        default=None,
    )
    version: str = Field(
        description="The version of the API",
        default="v1.1",
    )
    custom_instructions: Optional[str] = Field(
        description="Custom instructions for fact extraction",
        default=None,
    )


class AzureConfig(BaseModel):
    """
    Configuration settings for Azure.

    Args:
        api_key (str): The API key used for authenticating with the Azure service.
        azure_deployment (str): The name of the Azure deployment.
        azure_endpoint (str): The endpoint URL for the Azure service.
        api_version (str): The version of the Azure API being used.
        default_headers (Dict[str, str]): Headers to include in requests to the Azure API.
    """

    api_key: str = Field(
        description="The API key used for authenticating with the Azure service.",
        default=None,
    )
    azure_deployment: str = Field(description="The name of the Azure deployment.", default=None)
    azure_endpoint: str = Field(description="The endpoint URL for the Azure service.", default=None)
    api_version: str = Field(description="The version of the Azure API being used.", default=None)
    default_headers: Optional[Dict[str, str]] = Field(
        description="Headers to include in requests to the Azure API.", default=None
    )
