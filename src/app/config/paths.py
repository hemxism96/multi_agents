"""Renault Intelligence Agent - Path Configuration Module"""

from pathlib import Path


class PathConfig:
    """Path configuration management"""

    PROJECT_ROOT = str(Path(__file__).resolve().parents[3])

    DATA_DIR = f"{PROJECT_ROOT}/data"
    PDF_DIR = f"{DATA_DIR}/pdfs"
    VIDEO_SCRIPTS_DIR = f"{DATA_DIR}/video_scripts"

    DB_DIR = f"{PROJECT_ROOT}/db"
    CHROMA_DB_DIR = f"{DB_DIR}/chromadb"
