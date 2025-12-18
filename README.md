# Learning RAG Demo (Refactored)
This project is a refactored version of a simple Retrieval-Augmented Generation (RAG) demo API built with FastAPI.
The refactor focuses on clean architecture, maintainability, and testability, while preserving the original behavior.

The application allows:
- Adding documents (/add)

- Asking questions over stored documents (/ask)

- Checking system status (/status)

## Goals of the Refactor
The refactor prioritizes the following software engineering principles:

- **Encapsulation** – related data and behavior are grouped together

- **Separation of Concerns** – clear boundaries between web, business, and data layers

- **Explicit Dependencies** – no hidden globals; dependencies are passed explicitly

- **Testability** – business logic can be tested independently of FastAPI

- **Readability** – predictable structure, clear naming, minimal surprise

## Project Structure
```text
app/
├── main.py                     # Application entry point (composition root)
│
├── api/                        # Web / HTTP layer
│   ├── __init__.py
│   ├── routes.py               # FastAPI route definitions
│   └── schemas.py              # Request / response schemas
│
├── core/                       # Business logic (framework-agnostic)
│   ├── __init__.py
│   ├── service.py              # Application service (use-cases)
│   ├── workflow.py             # RAG retrieval → answer workflow
│   └── embeddings.py           # Embedding service abstraction
│
├── infrastructure/             # Data access / external integrations
│   ├── __init__.py
│   └── document_store.py       # Document storage implementation
│
└── dependencies.py             # Dependency construction/wiring
```

## Architecture Overview
This project follows a [Clean Architecture–inspired design](https://medium.com/@rafael-22/the-clean-architecture-i-wish-someone-had-explained-to-me-dcc1572dbeac).

## Dependency Direction

## Ket Components
### RagService (`app/core/service.py`)
Coordinates application use-cases:
- Adding documents
- Executing question-answering workflows
- Reporting system status

This class is:
- Framework-agnostic
- Easily unit-testable
- Explicitly injected with its dependencies

### RagWorkflow (`app/core/workflow.py`)
Implements the retrieval → answer pipeline.

Responsibilities:
- Generate query embeddings
- Retrieve relevant documents
- Produce a simple answer from context

### EmbeddingService (`app/core/embeddings.py`)
Abstracts embedding generation.

In this demo:
- Uses a deterministic fake embedding
- Can be replaced with a real model without touching business logic

### DocumentStore (`app/infrastructure/document_store.py`)
Handles document persistence and retrieval.

This separation allows:
- Swapping in-memory storage with Qdrant or another vector DB
- Isolated testing of storage logic

### **API Layer** (`app/api/routes.py`)
Defines HTTP endpoints:
- `/add`
- `/ask`
- `/status`

The API layer:
- Contains no business logic
- Delegates all work to RagService
- Translates exceptions into HTTP responses

### **Application Entry Point** (`app/main.py`)
This file is the composition root.

Responsibilities:
- Create the FastAPI app
- Construct dependencies
- Wire services together
- Register routes

No business logic lives here.

## How to Run
1. Create and activate virtual enviroment
    ```
    python -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```

2. Install dependencies
    ```
    pip install -r requirements.txt
    ```

3. Run the applications

    From the project root:
    ```
    uvicorn app.main:app --reload
    ```
    The API will be available at:
    ```
    http://127.0.0.1:8000
    ```
    Interactive API Docs:
    ```
    http://127.0.0.1:8000/docs
    ```
## Example API Usage
### Add a document
```
POST /add
{
  "text": "FastAPI is a modern Python web framework."
}
```

### Ask a qustion
```
POST /ask
{
  "question": "What is FastAPI?"
}
```

### Check status
```
GET /status
```

## Why This Design
This structure reflects real-world backend engineering practices:
- Clear ownership of responsibilities
- Minimal coupling
- Predictable import order
- Easy refactoring and extension
- Suitable for team-scale development