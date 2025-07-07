from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/all-MiniLM-l6-v2"
    chunk_size: int = 512
    max_tokens: int = 512
    chunk_overlap: int = 50


@dataclass
class LLMConfig:
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.0
    timeout: int = 30
    max_retries: int = 2


@dataclass
class RetrievalConfig:
    search_type: str = "mmr"
    k: int = 10
    collection_name: str = "db-rag"
