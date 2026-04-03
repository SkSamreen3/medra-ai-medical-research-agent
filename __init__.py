"""Tests for the Medical Research Agent."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.memory import MemoryManager
from app.models import Paper, PaperSource, Persona


client = TestClient(app)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def test_health():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "papers_indexed" in data


# ---------------------------------------------------------------------------
# Persona
# ---------------------------------------------------------------------------

def test_get_persona():
    resp = client.get("/persona")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "MedRA"


def test_update_persona():
    resp = client.put("/persona", json={"name": "Dr. Atlas", "tone": "friendly"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Dr. Atlas"
    assert data["tone"] == "friendly"

    # Reset
    client.put("/persona", json={"name": "MedRA", "tone": "professional, precise, and evidence-based"})


# ---------------------------------------------------------------------------
# Memory / profile
# ---------------------------------------------------------------------------

def test_add_interest():
    resp = client.post("/interests", json={"interest": "oncology"})
    assert resp.status_code == 200
    assert "oncology" in resp.json()["interests"]


def test_get_profile():
    resp = client.get("/profile")
    assert resp.status_code == 200
    assert "research_interests" in resp.json()


def test_conversation_history():
    resp = client.get("/history")
    assert resp.status_code == 200
    assert "history" in resp.json()

    resp = client.post("/history/clear")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Knowledge base
# ---------------------------------------------------------------------------

def test_kb_stats():
    resp = client.get("/knowledge-base/stats")
    assert resp.status_code == 200
    assert "total_papers" in resp.json()


# ---------------------------------------------------------------------------
# Model unit tests
# ---------------------------------------------------------------------------

def test_persona_system_prompt():
    p = Persona(name="TestBot", tone="casual", expertise=["cardiology"])
    prompt = p.to_system_prompt()
    assert "TestBot" in prompt
    assert "casual" in prompt
    assert "cardiology" in prompt


def test_paper_model():
    paper = Paper(
        title="Test Paper",
        authors=["Smith J"],
        abstract="Abstract text",
        source=PaperSource.PUBMED,
        source_id="12345",
    )
    assert paper.title == "Test Paper"
    assert paper.source == PaperSource.PUBMED


# ---------------------------------------------------------------------------
# Memory manager
# ---------------------------------------------------------------------------

def test_memory_manager():
    mem = MemoryManager(user_id="test_user")
    mem.add_message("user", "Hello")
    mem.add_message("assistant", "Hi there")

    history = mem.get_conversation_history()
    assert len(history) == 2
    assert history[0]["role"] == "user"

    mem.clear_short_term()
    assert len(mem.get_conversation_history()) == 0


def test_memory_interests():
    mem = MemoryManager(user_id="test_interests")
    mem.add_research_interest("neurology")
    assert "neurology" in mem.profile.research_interests

    # Duplicate should not be added
    mem.add_research_interest("neurology")
    assert mem.profile.research_interests.count("neurology") == 1


# ---------------------------------------------------------------------------
# Upload validation
# ---------------------------------------------------------------------------

def test_upload_non_pdf():
    from io import BytesIO

    resp = client.post(
        "/upload-pdf",
        files={"file": ("test.txt", BytesIO(b"not a pdf"), "text/plain")},
    )
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Query validation
# ---------------------------------------------------------------------------

def test_query_too_short():
    resp = client.post("/query", json={"query": "ab"})
    assert resp.status_code == 422  # validation error
