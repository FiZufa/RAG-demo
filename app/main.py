from fastapi import FastAPI

from app.api.routes import create_router
from app.dependencies import create_rag_service


def create_app() -> FastAPI:
    """
    Application factory.

    Responsible for:
    - creating FastAPI app
    - wiring dependencies
    - registering routes

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    app = FastAPI(title="Learning RAG Demo")

    rag_service = create_rag_service()
    app.include_router(create_router(rag_service))

    return app


app = create_app()
