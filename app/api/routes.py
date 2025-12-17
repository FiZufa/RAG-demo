import time
from typing import TYPE_CHECKING
from fastapi import APIRouter, HTTPException
from app.api.schemas import QuestionRequest, DocumentRequest

if TYPE_CHECKING:
    from app.core.service import RagService


def create_router(service: "RagService") -> APIRouter:
    """Create API routes for the RAG service."""

    router = APIRouter()

    @router.post("/add")
    def add(req: DocumentRequest):
        """
        Add a document to the RAG system.
        
        :param req: DocumentRequest containing the text to add
        :return: dict with document ID and status
        """

        try:
            return {"id": service.add_document(req.text), "status": "added"}
        except Exception as e:
            raise HTTPException(500, str(e))

    @router.post("/ask")
    def ask(req: QuestionRequest):
        """
        Ask a question to the RAG system.

        :param req: QuestionRequest containing the question
        :return: dict with question, answer, context used, and latency
        """

        start = time.time()
        try:
            result = service.ask(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise HTTPException(500, str(e))

    @router.get("/status")
    def status():
        """
        Get the status of the RAG service.

        :return: dict with service status information
        """
        return service.status()

    return router
