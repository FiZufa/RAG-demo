from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.core.embeddings import EmbeddingService
from app.infrastructure.document_store import DocumentStore


class RagWorkflow:
    """Retrieval → Answer pipeline."""

    def __init__(self, embedder: EmbeddingService, store: DocumentStore):
        """Initialize the RAG workflow."""

        self._embedder = embedder
        self._store = store
        self._graph = self._build()

    def _build(self):
        """Build the RAG workflow graph."""

        graph = StateGraph(dict)

        graph.add_node("retrieve", self._retrieve)
        graph.add_node("answer", self._answer)

        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)

        return graph.compile()

    def _retrieve(self, state: Dict[str, Any]):
        """Retrieve relevant context for the question."""

        embedding = self._embedder.embed(state["question"])
        state["context"] = self._store.search(embedding, limit=2)
        return state

    def _answer(self, state: Dict[str, Any]):
        """Generate an answer based on the retrieved context."""

        ctx = state.get("context", [])
        state["answer"] = (
            f"I found this: '{ctx[0][:100]}...'"
            if ctx else "Sorry, I don't know."
        )
        return state

    def run(self, question: str) -> Dict[str, Any]:
        """Run the RAG workflow for a given question."""
        
        return self._graph.invoke({"question": question})
