from typing import Any


DOCUMENTS = [
    {
        "id": "laptop-policy",
        "text": "Laptops have a standard warranty of 1 year.",
    },
    {
        "id": "phone-policy",
        "text": "Phones have a standard warranty of 2 years.",
    },
    {
        "id": "tablet-policy",
        "text": "Tablets have a standard warranty of 1 year.",
    },
]


class Retriever:
    """
    Simple keyword-based document retriever.
    """

    def retrieve(self, query: str) -> list[dict[str, Any]]:
        query_words = set(query.lower().split())

        results = []

        for document in DOCUMENTS:
            document_words = set(document["text"].lower().split())

            if query_words & document_words:
                results.append(document)

        return results