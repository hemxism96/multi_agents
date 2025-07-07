import os
from typing import Optional

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import YoutubeLoader
from data.video_list import video_list
from langchain_core.documents import Document
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker


def chunk_documents(documents: list, chunk_size: int = 512, chunk_overlap: int = 50) -> list:
    chunked_documents = []

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    for doc in documents:
        chunks = text_splitter.split_text(doc.page_content)
        for chunk in chunks:
            chunked_documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "filename": doc.metadata.get("origin", {}).get("filename", "")
                    }
                )
            )
    return chunked_documents


def load_youtube_video(from_url: bool = True, document_path: Optional[str] = None) -> list:
    """
    Load a YouTube video and return its documents.
    
    This function uses the YoutubeLoader to load a specific YouTube video
    and returns the documents extracted from it.
    
    Returns:
        list: A list of documents extracted from the YouTube video.
    """
    documents = []
    if from_url:
        documents = []
        for url in video_list.values():
            loader = YoutubeLoader.from_youtube_url(
                url,
                add_video_info=False,
                language=["en", "fr"]
            )
            doc = loader.load()
            documents.extend(doc)
    else:
        for file_name in os.listdir(document_path):
            path = os.path.join(document_path, file_name)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            doc = Document(
                page_content=content,
                metadata={
                    "origin": {"filename": file_name},
                }
            )
            documents.append(doc)

    return documents


def load_pdf_documents(document_path: str, embedding_model_name: str) -> list:
    """
    Load PDF documents from a specified directory.
    
    Args:
        document_path (str): The path to the directory containing PDF documents.
        
    Returns:
        list: A list of documents loaded from the PDF files.
    """
    file_paths = [
        os.path.join(document_path, file_name)
        for file_name in os.listdir(document_path)
        if file_name.endswith(".pdf")
    ]
    loader = DoclingLoader(
        file_path=file_paths,
        chunker=HybridChunker(
            tokenizer=embedding_model_name,
            max_tokens=512,
        ),
    )
    docs = loader.load()
    return docs


def build_vector_db(
    document_path: Optional[str] = "./data/pdfs",
    collection_name: Optional[str] = "db-rag",
    db_path: Optional[str] = "./db/chromadb",
    embedding_model_name: Optional[str] = "sentence-transformers/all-MiniLM-l6-v2"
) -> None:
    video_path = "/Users/suyeoncho/Documents/data_science/multi_agents/src/multi_agents/data/video_scripts"
    video_docs = load_youtube_video(from_url=False, document_path=video_path)
    pdf_docs = load_pdf_documents(document_path, embedding_model_name)
    documents = video_docs + pdf_docs

    documents = chunk_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    db = Chroma.from_documents(
        documents=documents,
        collection_name=collection_name,
        embedding=embeddings,
        persist_directory=db_path,
    )

if __name__ == "__main__":
    build_vector_db(
        document_path="/Users/suyeoncho/Documents/data_science/multi_agents/src/multi_agents/data/pdfs"
    )

