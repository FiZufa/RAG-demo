from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.settings import QDRANT_URL, QDRANT_COLLECTION, VECTOR_SIZE
from app.core.embeddings import EmbeddingService
from app.infrastructure.document_store import (
    InMemoryDocumentStore,
    QdrantDocumentStore,
)
from app.core.workflow import RagWorkflow
from app.core.service import RagService


def create_rag_service() -> RagService:
    """
    Create and configure the RAG service with appropriate dependencies.

    :return: Configured RagService instance
    :rtype: RagService
    """
    embedder = EmbeddingService()

    try:
        client = QdrantClient(QDRANT_URL)
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )
        store = QdrantDocumentStore(client)
    except Exception:
        store = InMemoryDocumentStore()

    workflow = RagWorkflow(embedder, store)
    return RagService(embedder, store, workflow)
