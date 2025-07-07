import logging

logger = logging.getLogger(__name__)

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from app.config import RetrievalConfig, PathConfig, EmbeddingConfig
from app.utils import error_handler


class RetrieverArgs(BaseModel):
    question: str = Field(
        description="The original user question to retrieve relevant documents for"
    )


def get_retriever() -> VectorStoreRetriever:
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


def retrieve(question: str):
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
