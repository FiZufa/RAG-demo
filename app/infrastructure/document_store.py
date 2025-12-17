from typing import List
from abc import ABC, abstractmethod
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.settings import QDRANT_COLLECTION


class DocumentStore(ABC):
    """Abstract interface for document persistence."""

    @abstractmethod
    def add(self, doc_id: int, text: str, embedding: List[float]) -> None:
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], limit: int) -> List[str]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class InMemoryDocumentStore(DocumentStore):
    """Simple in-memory document store."""
    
    def __init__(self):
        """Initialize InMemoryDocumentStore."""
        self._docs: List[str] = []

    def add(self, doc_id: int, text: str, embedding: List[float]) -> None:
        """Add a document to the store."""
        self._docs.append(text)

    def search(self, query_embedding: List[float], limit: int) -> List[str]:
        """Search for documents in the store."""
        return self._docs[:limit]

    def count(self) -> int:
        return len(self._docs)
