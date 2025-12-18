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


class QdrantDocumentStore(DocumentStore):
    """Document store backed by a Qdrant vector database."""

    def __init__(self, client: QdrantClient, collection_name: str = QDRANT_COLLECTION):
        """Initialize with a `QdrantClient` and optional collection name."""
        self._client = client
        self._collection = collection_name

    def add(self, doc_id: int, text: str, embedding: List[float]) -> None:
        """Upsert a single document as a point into Qdrant."""
        point = PointStruct(id=doc_id, vector=embedding, payload={"text": text})
        self._client.upsert(collection_name=self._collection, points=[point])

    def search(self, query_embedding: List[float], limit: int) -> List[str]:
        """Search Qdrant for nearest vectors and return stored texts."""
        hits = self._client.search(
            collection_name=self._collection,
            query_vector=query_embedding,
            limit=limit,
        )
        results: List[str] = []
        for hit in hits:
            payload = getattr(hit, "payload", None) or {}
            text = payload.get("text")
            if text:
                results.append(text)
        return results

    def count(self) -> int:
        """Return number of points in the collection (0 on error)."""
        try:
            res = self._client.count(collection_name=self._collection)
            return int(getattr(res, "count", 0))
        except Exception:
            return 0
