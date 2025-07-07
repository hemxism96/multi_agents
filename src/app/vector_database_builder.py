"""
This module builds a vector database from YouTube transcripts and PDF documents.
It handles loading, chunking, and embedding of documents to create a searchable vector store.
"""

import os
from typing import List, Optional

from config import EmbeddingConfig, PathConfig, RetrievalConfig
from config.youtube_urls import urls
from docling.chunking import HybridChunker
from langchain_chroma import Chroma
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.documents import Document
from langchain_docling import DoclingLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import error_handler


class VectorDatabaseBuilder:
    """
    A comprehensive class for building vector databases from YouTube transcripts and PDF documents.
    """

    def __init__(
        self,
        embedding_model_name: str = EmbeddingConfig.model_name,
        chunk_size: int = EmbeddingConfig.chunk_size,
        chunk_overlap: int = EmbeddingConfig.chunk_overlap,
        max_tokens: int = EmbeddingConfig.max_tokens,
        db_path: str = PathConfig.CHROMA_DB_DIR,
    ):
        """
        Initialize the VectorDatabaseBuilder.

        Args:
            embedding_model_name: Name of the embedding model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            max_tokens: Maximum tokens per chunk
            db_path: Path to store the database
        """
        self.embedding_model_name = embedding_model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.max_tokens = max_tokens
        self.db_path = db_path

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)

    def split_documents_into_chunks(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better embedding performance.

        Args:
            documents: List of documents to be chunked

        Returns:
            List of chunked documents
        """
        chunked_documents = []

        for doc in documents:
            try:
                chunks = self.text_splitter.split_text(doc.page_content)
                for chunk in chunks:
                    chunked_documents.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "filename": doc.metadata.get("origin", {}).get(
                                    "filename", "unknown"
                                ),
                                "source": doc.metadata.get("source", "unknown"),
                                "doc_type": self._detect_document_type(doc),
                            },
                        )
                    )
            except Exception as e:
                print(f"Error processing document: {e}")
                continue

        return chunked_documents

    def load_youtube_transcripts(
        self, from_url: bool = False, document_path: Optional[str] = None
    ) -> List[Document]:
        """
        Load YouTube transcripts either from URLs or local files.

        Args:
            from_url: Whether to load from YouTube URLs or local files
            document_path: Path to local transcript files

        Returns:
            List of loaded documents
        """
        documents = []

        if from_url:
            for url in urls.values():
                try:
                    loader = YoutubeLoader.from_youtube_url(
                        url, add_video_info=False, language=["en", "fr"]
                    )
                    doc = loader.load()
                    print(doc)
                    documents.extend(doc)
                except Exception as e:
                    print(f"Error loading YouTube video from {url}: {e}")
                    continue
        else:
            try:
                for file_name in os.listdir(document_path):
                    file_path = os.path.join(document_path, file_name)
                    if os.path.isfile(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        doc = Document(
                            page_content=content,
                            metadata={
                                "origin": {"filename": file_name},
                                "source": "youtube_transcript",
                            },
                        )
                        documents.append(doc)
            except Exception as e:
                print(f"Error reading local files: {e}")

        return documents

    def load_pdf_files(self, document_path: str) -> List[Document]:
        """
        Load PDF documents using DoclingLoader.

        Args:
            document_path: Path to directory containing PDF files

        Returns:
            List of loaded PDF documents
        """
        try:
            file_paths = [
                os.path.join(document_path, file_name)
                for file_name in os.listdir(document_path)
                if file_name.endswith(".pdf")
            ]

            loader = DoclingLoader(
                file_path=file_paths,
                chunker=HybridChunker(
                    tokenizer=self.embedding_model_name,
                    max_tokens=self.max_tokens,
                ),
            )
            docs = loader.load()
            return docs
        except Exception as e:
            print(f"Error loading PDF files: {e}")
            return []

    def create_vector_database(
        self,
        load_from_url: bool = False,
        video_path: str = PathConfig.VIDEO_SCRIPTS_DIR,
        pdf_path: str = PathConfig.PDF_DIR,
        collection_name: str = RetrievalConfig.collection_name,
    ) -> Optional[Chroma]:
        """
        Create a vector database from YouTube transcripts and PDF documents.

        Args:
            load_from_url: Whether to load YouTube videos from URLs
            video_path: Path to local video transcript files
            pdf_path: Path to PDF documents
            collection_name: Name of the collection in the database

        Returns:
            Chroma vector database instance or None if creation failed
        """
        try:
            # Load documents
            video_docs = self.load_youtube_transcripts(
                from_url=load_from_url, document_path=video_path
            )
            pdf_docs = self.load_pdf_files(pdf_path)

            # Combine documents
            documents = video_docs + pdf_docs

            if not documents:
                print("No documents loaded. Aborting database creation.")
                return None

            # Chunk documents
            documents = self.split_documents_into_chunks(documents)

            db = Chroma.from_documents(
                documents=documents,
                collection_name=collection_name,
                embedding=self.embeddings,
                persist_directory=self.db_path,
            )

            return db

        except Exception as e:
            print(f"Error creating vector database: {e}")
            return None

    def _detect_document_type(self, doc: Document) -> str:
        """
        Detect document type based on source.

        Args:
            doc: Document to analyze

        Returns:
            Document type string
        """
        source = doc.metadata.get("source", "").lower()
        if "youtube" in source:
            return "youtube_transcript"
        if source.endswith(".pdf"):
            return "pdf"
        return "unknown"


def main():
    """Main function to demonstrate vector database creation."""
    # Create builder instance
    builder = VectorDatabaseBuilder()

    # Create database
    db = builder.create_vector_database()

    if db:
        print("Vector database created successfully")
    else:
        print("Failed to create vector database.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        error_handler(e)
