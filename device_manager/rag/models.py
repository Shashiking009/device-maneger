from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    path: str
    filename: str
    extension: str
    text: str
    size_bytes: int
    modified_time: float
    document_hash: str

class ChunkMetadata(BaseModel):
    document_id: str
    chunk_id: str
    source_path: str
    filename: str
    extension: str
    chunk_index: int
    content_hash: str
    document_hash: str
    created_at: float
    modified_at: float

class Chunk(BaseModel):
    id: str
    text: str
    metadata: ChunkMetadata

class SearchResult(BaseModel):
    content: str
    source_path: str
    filename: str
    score: float
    chunk_id: str
    extension: str

class RAGQueryResponse(BaseModel):
    success: bool
    answer: str
    sources: List[str]
    search_results: List[SearchResult] = Field(default_factory=list)
    tps: Optional[float] = None
    query_time_ms: float = 0.0

class IndexingManifest(BaseModel):
    documents: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    total_chunks: int = 0
    last_updated: float = 0.0

class RAGStatusResponse(BaseModel):
    ready: bool
    status: str
    documents_count: int
    chunks_count: int
    embedding_model: str
    vector_store: str
    persistent: bool
