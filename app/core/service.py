from app.core.workflow import RagWorkflow
from app.core.embeddings import EmbeddingService
from app.infrastructure.document_store import DocumentStore


class RagService:
    """Coordinates application use-cases."""

    def __init__(
        self,
        embedder: EmbeddingService,
        store: DocumentStore,
        workflow: RagWorkflow,
    ):
        self._embedder = embedder
        self._store = store
        self._workflow = workflow
        self._doc_id = 0

    def add_document(self, text: str) -> int:
        """Add a document to the store and return its ID."""

        embedding = self._embedder.embed(text)
        doc_id = self._doc_id
        self._doc_id += 1
        self._store.add(doc_id, text, embedding)
        return doc_id

    def ask(self, question: str):
        """Ask a question to the RAG system."""

        return self._workflow.run(question)

    def status(self):
        """Get the status of the RAG service."""
        
        return {
            "in_memory_docs_count": self._store.count(),
            "graph_ready": True,
        }
