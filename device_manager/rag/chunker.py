import re
import time
import hashlib
from typing import List
from rag.config import CHUNK_SIZE, CHUNK_OVERLAP
from rag.models import Document, Chunk, ChunkMetadata

class IntelligentChunker:
    """
    Intelligent document chunker with structure-aware splitting for Markdown, Python, and Text.
    Attaches complete SHA-256 chunk metadata.
    """
    def __init__(self, target_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
        self.target_size = target_size
        self.overlap = overlap

    def chunk_document(self, doc: Document) -> List[Chunk]:
        ext = doc.extension.lower()
        if ext == ".md":
            raw_chunks = self._chunk_markdown(doc.text)
        elif ext == ".py":
            raw_chunks = self._chunk_python(doc.text)
        else:
            raw_chunks = self._chunk_text(doc.text)

        chunks = []
        now = time.time()
        for idx, text_block in enumerate(raw_chunks):
            if not text_block.strip():
                continue

            chunk_id = f"{doc.document_hash[:12]}_{idx}"
            content_hash = hashlib.sha256(text_block.encode('utf-8')).hexdigest()

            meta = ChunkMetadata(
                document_id=doc.document_hash,
                chunk_id=chunk_id,
                source_path=doc.path,
                filename=doc.filename,
                extension=doc.extension,
                chunk_index=idx,
                content_hash=content_hash,
                document_hash=doc.document_hash,
                created_at=now,
                modified_at=doc.modified_time
            )

            chunks.append(Chunk(id=chunk_id, text=text_block, metadata=meta))

        return chunks

    def _chunk_markdown(self, text: str) -> List[str]:
        # Split by Markdown headings #, ##, ###
        sections = re.split(r'\n(?=#+ )', text)
        result = []
        for sec in sections:
            if len(sec) > self.target_size:
                result.extend(self._chunk_text(sec))
            else:
                result.append(sec.strip())
        return result

    def _chunk_python(self, text: str) -> List[str]:
        # Split by top-level class or def blocks
        blocks = re.split(r'\n(?=(?:class|def)\s+)', text)
        result = []
        for blk in blocks:
            if len(blk) > self.target_size:
                result.extend(self._chunk_text(blk))
            else:
                result.append(blk.strip())
        return result

    def _chunk_text(self, text: str) -> List[str]:
        paragraphs = text.split('\n\n')
        chunks = []
        current = ""

        for p in paragraphs:
            p_str = p.strip()
            if not p_str:
                continue
            if len(current) + len(p_str) <= self.target_size:
                current = f"{current}\n\n{p_str}" if current else p_str
            else:
                if current:
                    chunks.append(current.strip())
                current = p_str

        if current:
            chunks.append(current.strip())

        return chunks

chunker = IntelligentChunker()
