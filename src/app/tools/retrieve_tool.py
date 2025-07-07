"""Renault Intelligence Agent - Document Retrieval Tool Module
This module provides a tool to retrieve relevant documents from a vector store
using a question as input. It utilizes the Chroma vector store and HuggingFace embeddings for
document retrieval."""

import logging

logger = logging.getLogger(__name__)

import chromadb
from langchain.tools import StructuredTool
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

from config import EmbeddingConfig, PathConfig, RetrievalConfig
from utils import error_handler


class RetrieverArgs(BaseModel):
    """Arguments for retrieving documents."""

    question: str = Field(
        description="The original user question to retrieve relevant documents for"
    )


def get_retriever() -> VectorStoreRetriever:
    """Initialize and return a retriever for document retrieval."""
    embeddings = HuggingFaceEmbeddings(model_name=EmbeddingConfig.model_name)
    persistent_client = chromadb.PersistentClient(path=PathConfig.CHROMA_DB_DIR)
    db = Chroma(
        client=persistent_client,
        embedding_function=embeddings,
        collection_name=RetrievalConfig.collection_name,
    )
    retriever = db.as_retriever(
        search_type=RetrievalConfig.search_type, search_kwargs={"k": RetrievalConfig.k}
    )
    return retriever


def retrieve(question: str) -> str:
    """Retrieve documents relevant to the provided question."""
    logger.info(f"Retrieving documents")
    try:
        retriever = get_retriever()
        documents = retriever.invoke(question)

        return "\n".join([f"- {doc}" for doc in documents])
    except Exception as e:
        error_handler(e)
        return "An error occurred while retrieving documents."


retriever_tool = StructuredTool.from_function(
    func=retrieve,
    name="retrieve_documents",
    description="Retrieve relevant documents to answer the question.",
    args_schema=RetrieverArgs,
    return_direct=False,
)
