import importlib
from typing import Dict, Optional, Union

from dejavu.configs.embeddings.base import BaseEmbedderConfig
from dejavu.configs.llms.anthropic import AnthropicConfig
from dejavu.configs.llms.aws_bedrock import AWSBedrockConfig
from dejavu.configs.llms.azure import AzureOpenAIConfig
from dejavu.configs.llms.base import BaseLlmConfig
from dejavu.configs.llms.deepseek import DeepSeekConfig
from dejavu.configs.llms.minimax import MinimaxConfig
from dejavu.configs.llms.lmstudio import LMStudioConfig
from dejavu.configs.llms.ollama import OllamaConfig
from dejavu.configs.llms.openai import OpenAIConfig
from dejavu.configs.llms.venice import VeniceConfig
from dejavu.configs.llms.vllm import VllmConfig
from dejavu.configs.rerankers.base import BaseRerankerConfig
from dejavu.configs.rerankers.cohere import CohereRerankerConfig
from dejavu.configs.rerankers.sentence_transformer import SentenceTransformerRerankerConfig
from dejavu.configs.rerankers.zero_entropy import ZeroEntropyRerankerConfig
from dejavu.configs.rerankers.llm import LLMRerankerConfig
from dejavu.configs.rerankers.huggingface import HuggingFaceRerankerConfig
from dejavu.embeddings.mock import MockEmbeddings


def load_class(class_type):
    module_path, class_name = class_type.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class LlmFactory:
    """
    Factory for creating LLM instances with appropriate configurations.
    Supports both old-style BaseLlmConfig and new provider-specific configs.
    """

    # Provider mappings with their config classes
    provider_to_class = {
        "venice": ("dejavu.llms.venice.VeniceLLM", VeniceConfig),
        "ollama": ("dejavu.llms.ollama.OllamaLLM", OllamaConfig),
        "openai": ("dejavu.llms.openai.OpenAILLM", OpenAIConfig),
        "groq": ("dejavu.llms.groq.GroqLLM", BaseLlmConfig),
        "together": ("dejavu.llms.together.TogetherLLM", BaseLlmConfig),
        "aws_bedrock": ("dejavu.llms.aws_bedrock.AWSBedrockLLM", AWSBedrockConfig),
        "litellm": ("dejavu.llms.litellm.LiteLLM", BaseLlmConfig),
        "azure_openai": ("dejavu.llms.azure_openai.AzureOpenAILLM", AzureOpenAIConfig),
        "openai_structured": ("dejavu.llms.openai_structured.OpenAIStructuredLLM", OpenAIConfig),
        "anthropic": ("dejavu.llms.anthropic.AnthropicLLM", AnthropicConfig),
        "azure_openai_structured": ("dejavu.llms.azure_openai_structured.AzureOpenAIStructuredLLM", AzureOpenAIConfig),
        "gemini": ("dejavu.llms.gemini.GeminiLLM", BaseLlmConfig),
        "deepseek": ("dejavu.llms.deepseek.DeepSeekLLM", DeepSeekConfig),
        "minimax": ("dejavu.llms.minimax.MiniMaxLLM", MinimaxConfig),
        "xai": ("dejavu.llms.xai.XAILLM", BaseLlmConfig),
        "sarvam": ("dejavu.llms.sarvam.SarvamLLM", BaseLlmConfig),
        "lmstudio": ("dejavu.llms.lmstudio.LMStudioLLM", LMStudioConfig),
        "vllm": ("dejavu.llms.vllm.VllmLLM", VllmConfig),
        "langchain": ("dejavu.llms.langchain.LangchainLLM", BaseLlmConfig),
    }

    @classmethod
    def create(cls, provider_name: str, config: Optional[Union[BaseLlmConfig, Dict]] = None, **kwargs):
        """
        Create an LLM instance with the appropriate configuration.

        Args:
            provider_name (str): The provider name (e.g., 'openai', 'anthropic')
            config: Configuration object or dict. If None, will create default config
            **kwargs: Additional configuration parameters

        Returns:
            Configured LLM instance

        Raises:
            ValueError: If provider is not supported
        """
        if provider_name not in cls.provider_to_class:
            raise ValueError(f"Unsupported Llm provider: {provider_name}")

        class_type, config_class = cls.provider_to_class[provider_name]
        llm_class = load_class(class_type)

        # Handle configuration
        if config is None:
            # Create default config with kwargs
            config = config_class(**kwargs)
        elif isinstance(config, dict):
            # Merge dict config with kwargs
            config.update(kwargs)
            config = config_class(**config)
        elif isinstance(config, BaseLlmConfig):
            # Convert base config to provider-specific config if needed
            if config_class != BaseLlmConfig:
                # Convert to provider-specific config
                config_dict = {
                    "model": config.model,
                    "temperature": config.temperature,
                    "api_key": config.api_key,
                    "max_tokens": config.max_tokens,
                    "top_p": config.top_p,
                    "top_k": config.top_k,
                    "enable_vision": config.enable_vision,
                    "vision_details": config.vision_details,
                    "http_client_proxies": config.http_client,
                }
                config_dict.update(kwargs)
                config = config_class(**config_dict)
            else:
                # Use base config as-is
                pass
        else:
            # Assume it's already the correct config type
            pass

        return llm_class(config)

    @classmethod
    def register_provider(cls, name: str, class_path: str, config_class=None):
        """
        Register a new provider.

        Args:
            name (str): Provider name
            class_path (str): Full path to LLM class
            config_class: Configuration class for the provider (defaults to BaseLlmConfig)
        """
        if config_class is None:
            config_class = BaseLlmConfig
        cls.provider_to_class[name] = (class_path, config_class)

    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Get list of supported providers.

        Returns:
            list: List of supported provider names
        """
        return list(cls.provider_to_class.keys())


class EmbedderFactory:
    provider_to_class = {
        "openai": "dejavu.embeddings.openai.OpenAIEmbedding",
        "ollama": "dejavu.embeddings.ollama.OllamaEmbedding",
        "huggingface": "dejavu.embeddings.huggingface.HuggingFaceEmbedding",
        "azure_openai": "dejavu.embeddings.azure_openai.AzureOpenAIEmbedding",
        "gemini": "dejavu.embeddings.gemini.GoogleGenAIEmbedding",
        "vertexai": "dejavu.embeddings.vertexai.VertexAIEmbedding",
        "together": "dejavu.embeddings.together.TogetherEmbedding",
        "lmstudio": "dejavu.embeddings.lmstudio.LMStudioEmbedding",
        "langchain": "dejavu.embeddings.langchain.LangchainEmbedding",
        "aws_bedrock": "dejavu.embeddings.aws_bedrock.AWSBedrockEmbedding",
        "fastembed": "dejavu.embeddings.fastembed.FastEmbedEmbedding",
    }

    @classmethod
    def create(cls, provider_name, config, vector_config: Optional[dict]):
        if provider_name == "upstash_vector" and vector_config and vector_config.enable_embeddings:
            return MockEmbeddings()
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            embedder_instance = load_class(class_type)
            base_config = BaseEmbedderConfig(**config)
            return embedder_instance(base_config)
        else:
            raise ValueError(f"Unsupported Embedder provider: {provider_name}")


class VectorStoreFactory:
    provider_to_class = {
        "qdrant": "dejavu.vector_stores.qdrant.Qdrant",
        "chroma": "dejavu.vector_stores.chroma.ChromaDB",
        "pgvector": "dejavu.vector_stores.pgvector.PGVector",
        "milvus": "dejavu.vector_stores.milvus.MilvusDB",
        "upstash_vector": "dejavu.vector_stores.upstash_vector.UpstashVector",
        "azure_ai_search": "dejavu.vector_stores.azure_ai_search.AzureAISearch",
        "azure_mysql": "dejavu.vector_stores.azure_mysql.AzureMySQL",
        "pinecone": "dejavu.vector_stores.pinecone.PineconeDB",
        "mongodb": "dejavu.vector_stores.mongodb.MongoDB",
        "redis": "dejavu.vector_stores.redis.RedisDB",
        "valkey": "dejavu.vector_stores.valkey.ValkeyDB",
        "databricks": "dejavu.vector_stores.databricks.Databricks",
        "elasticsearch": "dejavu.vector_stores.elasticsearch.ElasticsearchDB",
        "vertex_ai_vector_search": "dejavu.vector_stores.vertex_ai_vector_search.GoogleMatchingEngine",
        "opensearch": "dejavu.vector_stores.opensearch.OpenSearchDB",
        "supabase": "dejavu.vector_stores.supabase.Supabase",
        "weaviate": "dejavu.vector_stores.weaviate.Weaviate",
        "faiss": "dejavu.vector_stores.faiss.FAISS",
        "langchain": "dejavu.vector_stores.langchain.Langchain",
        "s3_vectors": "dejavu.vector_stores.s3_vectors.S3Vectors",
        "baidu": "dejavu.vector_stores.baidu.BaiduDB",
        "cassandra": "dejavu.vector_stores.cassandra.CassandraDB",
        "neptune": "dejavu.vector_stores.neptune_analytics.NeptuneAnalyticsVector",
        "turbopuffer": "dejavu.vector_stores.turbopuffer.TurbopufferDB",
    }

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            if not isinstance(config, dict):
                config = config.model_dump()
            vector_store_instance = load_class(class_type)
            return vector_store_instance(**config)
        else:
            raise ValueError(f"Unsupported VectorStore provider: {provider_name}")

    @classmethod
    def reset(cls, instance):
        instance.reset()
        return instance



class RerankerFactory:
    """
    Factory for creating reranker instances with appropriate configurations.
    Supports provider-specific configs following the same pattern as other factories.
    """

    # Provider mappings with their config classes
    provider_to_class = {
        "cohere": ("dejavu.reranker.cohere_reranker.CohereReranker", CohereRerankerConfig),
        "sentence_transformer": ("dejavu.reranker.sentence_transformer_reranker.SentenceTransformerReranker", SentenceTransformerRerankerConfig),
        "zero_entropy": ("dejavu.reranker.zero_entropy_reranker.ZeroEntropyReranker", ZeroEntropyRerankerConfig),
        "llm_reranker": ("dejavu.reranker.llm_reranker.LLMReranker", LLMRerankerConfig),
        "huggingface": ("dejavu.reranker.huggingface_reranker.HuggingFaceReranker", HuggingFaceRerankerConfig),
    }

    @classmethod
    def create(cls, provider_name: str, config: Optional[Union[BaseRerankerConfig, Dict]] = None, **kwargs):
        """
        Create a reranker instance based on the provider and configuration.

        Args:
            provider_name: The reranker provider (e.g., 'cohere', 'sentence_transformer')
            config: Configuration object or dictionary
            **kwargs: Additional configuration parameters

        Returns:
            Reranker instance configured for the specified provider

        Raises:
            ImportError: If the provider class cannot be imported
            ValueError: If the provider is not supported
        """
        if provider_name not in cls.provider_to_class:
            raise ValueError(f"Unsupported reranker provider: {provider_name}")

        class_path, config_class = cls.provider_to_class[provider_name]

        # Handle configuration
        if config is None:
            config = config_class(**kwargs)
        elif isinstance(config, dict):
            config = config_class(**config, **kwargs)
        elif not isinstance(config, BaseRerankerConfig):
            raise ValueError(f"Config must be a {config_class.__name__} instance or dict")

        # Import and create the reranker class
        try:
            reranker_class = load_class(class_path)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not import reranker for provider '{provider_name}': {e}")

        return reranker_class(config)
