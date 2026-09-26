from unittest.mock import MagicMock

from app.services.rag import RAGService


def test_rag_empty_retrieval_returns_ungrounded_boundary():
    service = RAGService()
    service.retriever = MagicMock()
    service.retriever.retrieve.return_value = []

    res = service.generate_advisory(query="Unknown disease query XYZ")
    assert res["provider"] == "rag-grounding-boundary"
    assert "No authoritative" in res["recommendation"]
    assert res["citations"] == []


def test_rag_citation_integrity_without_fake_urls():
    service = RAGService()
    service.retriever = MagicMock()
    service.retriever.retrieve.return_value = [
        {
            "title": "Custom Pest Advisory",
            "organization": "State Ag Dept",
            "content": "Apply neem oil for early aphid control.",
            "document_id": "doc_101",
            "url": None,  # Missing URL
        }
    ]

    res = service.generate_advisory(query="aphids")
    assert len(res["citations"]) == 1
    cit = res["citations"][0]
    assert cit.title == "Custom Pest Advisory"
    assert cit.organization == "State Ag Dept"
    assert cit.url is None  # Must stay None, not fabricated into https://icar.org.in/
