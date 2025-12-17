import random
from typing import List
from app.settings import VECTOR_SIZE


class EmbeddingService:
    """Responsible only for text → vector transformation."""

    def embed(self, text: str) -> List[float]:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(VECTOR_SIZE)]
