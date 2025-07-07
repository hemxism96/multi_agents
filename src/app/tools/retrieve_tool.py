from typing import Optional

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class RetrieverArgs(BaseModel):
    question: str = Field(description="The question to retrieve relevant documents for.")

def get_retriever(
    collection_name: Optional[str] = "db-rag",
    db_path: Optional[str] = "./db/chromadb",
    embedding_model_name: Optional[str] = "sentence-transformers/all-MiniLM-l6-v2"
) -> None:
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    persistent_client = chromadb.PersistentClient(path=db_path)
    db = Chroma(
        client=persistent_client,
        embedding_function=embeddings,
        collection_name = collection_name
    )
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 10}
    )
    return retriever

def retrieve(question: str):
    print("===RETRIEVAL===")
    retriever = get_retriever()
    documents = retriever.invoke(question)

    return "\n".join([f"- {doc}" for doc in documents])

retriever_tool = StructuredTool.from_function(
    func=retrieve,
    name="retrieve_documents",
    description="Retrieve relevant documents to answer the question.",
    args_schema=RetrieverArgs,
    return_direct=False
)