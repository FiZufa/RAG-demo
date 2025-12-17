from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Request schema for asking a question."""

    question: str


class DocumentRequest(BaseModel):
    """Request schema for adding a document."""
    
    text: str
