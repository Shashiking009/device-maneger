import os
import hashlib
import fnmatch
from pathlib import Path
from typing import Optional
from rag.config import MAX_DOCUMENT_SIZE_MB, SUPPORTED_EXTENSIONS, SENSITIVE_EXCLUSION_PATTERNS
from rag.models import Document
from rag.cleaner import cleaner

class DocumentLoader:
    """
    Unified loader for local files (.txt, .md, .py, .json, .csv).
    Enforces security exclusions, path normalization, and SHA-256 hashing.
    """
    def __init__(self, max_size_mb: float = MAX_DOCUMENT_SIZE_MB):
        self.max_bytes = int(max_size_mb * 1024 * 1024)

    def is_sensitive(self, filename: str) -> bool:
        lower_name = filename.lower()
        for pattern in SENSITIVE_EXCLUSION_PATTERNS:
            if fnmatch.fnmatch(lower_name, pattern):
                return True
        return False

    def load(self, filepath: str) -> Optional[Document]:
        path = Path(filepath).resolve()
        
        # Check path existence
        if not path.is_file():
            return None

        filename = path.name
        ext = path.suffix.lower()

        # Security check: extension & sensitive file exclusion
        if ext not in SUPPORTED_EXTENSIONS or self.is_sensitive(filename):
            return None

        # Check size limit
        size = path.stat().st_size
        if size > self.max_bytes or size == 0:
            return None

        # Read content bytes & compute SHA-256 hash
        try:
            with open(path, "rb") as f:
                content_bytes = f.read()
            doc_hash = hashlib.sha256(content_bytes).hexdigest()
        except Exception:
            return None

        # Attempt decoding UTF-8, UTF-8-BOM, latin-1
        text = ""
        for encoding in ["utf-8", "utf-8-sig", "latin-1"]:
            try:
                text = content_bytes.decode(encoding)
                break
            except Exception:
                continue

        if not text:
            return None

        cleaned_text = cleaner.clean(text, ext)
        if not cleaned_text:
            return None

        return Document(
            path=str(path),
            filename=filename,
            extension=ext,
            text=cleaned_text,
            size_bytes=size,
            modified_time=path.stat().st_mtime,
            document_hash=doc_hash
        )

loader = DocumentLoader()
