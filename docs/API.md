# 🚀 MedRA v2.0 API Documentation

**Base URL:** `http://localhost:8000`

---

## Table of Contents

1. [Health & Info](#health--info)
2. [Query (Core)](#query-core)
3. [Knowledge Base](#knowledge-base)
4. [Persona & Memory](#persona--memory)
5. [Evaluation](#evaluation)
6. [Admin](#admin)

---

## Health & Info

### GET `/`
Health check with system statistics.

**Response:**
```json
{
  "status": "healthy",
  "papers_indexed": 42,
  "model": "gpt-4o",
  "version": "2.0.0",
  "evaluation_enabled": true
}
```

---

### GET `/health`
Detailed health status.

**Response:**
```json
{
  "status": "ok",
  "llm_provider": "openai",
  "vector_db": "ChromaDB",
  "evaluation": true,
  "papers": 42
}
```

---

## Query (Core)

### POST `/query`
Submit a research query to the multi-agent system.

**Request:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest treatments for Parkinson'\''s disease?",
    "user_id": "user123",
    "evaluate": true
  }'
```

**Request Body:**
```json
{
  "query": "string (required, 3-2000 chars)",
  "user_id": "string (optional, default: 'default')",
  "evaluate": "boolean (optional, default: false)"
}
```

**Response (200 OK):**
```json
{
  "answer": "## Parkinson's Disease — Latest Treatments\n\n...",
  "reasoning_steps": [
    {
      "thought": "I need to search for recent Parkinson's treatment papers",
      "action": "search_papers",
      "action_input": {"query": "Parkinson's treatment"},
      "observation": "Found 15 papers",
      "agent": "research"
    },
    {
      "thought": "Now I'll summarize the key findings",
      "action": "summarize",
      "observation": "Extracted 5 main treatments",
      "agent": "summarizer"
    }
  ],
  "papers_used": [
    {
      "id": "abc123",
      "title": "Novel Dopamine Replacement Strategies for Parkinson's",
      "authors": ["Smith, J.", "Johnson, M."],
      "abstract": "...",
      "source": "pubmed",
      "source_id": "12345678",
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
      "publication_date": "2024-03-15",
      "journal": "Nature Neuroscience",
      "doi": "10.1038/nn.1234"
    }
  ],
  "sources": [
    {
      "paper_id": "abc123",
      "paper_title": "Novel Dopamine Replacement Strategies...",
      "authors": ["Smith, J."],
      "source_url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
      "doi": "10.1038/nn.1234",
      "relevance_score": 0.95
    }
  ],
  "confidence": 0.92,
  "evaluation": {
    "faithfulness": 0.95,
    "answer_relevancy": 0.88,
    "context_relevancy": 0.89,
    "hallucination_score": 0.12,
    "correctness": 0.91,
    "evaluation_notes": "RAGAS evaluation completed"
  },
  "treatments_found": ["Levodopa", "Deep Brain Stimulation", "Gene therapy"],
  "drugs_found": ["Carbidopa", "Bromocriptine"],
  "key_findings": [
    "DBS effectiveness varies by patient",
    "Gene therapy shows promise",
    "Combination therapy most effective"
  ],
  "query": "What are the latest treatments for Parkinson's disease?",
  "agent_names": ["research", "summarizer", "analyzer", "critic", "memory"],
  "execution_time_ms": 3245.5,
  "medical_disclaimer": "⚠️ MEDICAL DISCLAIMER: This response is for educational and research purposes only..."
}
```

**Error (500):**
```json
{
  "detail": "Error message"
}
```

---

## Knowledge Base

### GET `/knowledge-base/stats`
Get knowledge base statistics.

**Response:**
```json
{
  "total_papers": 42,
  "vector_db": "ChromaDB",
  "embeddings": "text-embedding-3-large"
}
```

---

### POST `/upload-pdf`
Upload and index a PDF paper.

**Request:**
```bash
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@research_paper.pdf" \
  -F "user_id=user123"
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Paper indexed successfully",
  "paper_title": "Novel Treatment Approaches for Type 2 Diabetes",
  "papers_indexed": 1,
  "total_papers": 43
}
```

**Error (400):**
```json
{
  "detail": "Only PDF files accepted"
}
```

---

### POST `/knowledge-base/clear`
Clear all papers from knowledge base (admin).

**Request:**
```bash
curl -X POST http://localhost:8000/knowledge-base/clear
```

**Response:**
```json
{
  "status": "cleared",
  "total_papers": 0
}
```

---

## Persona & Memory

### GET `/persona`
Get current agent persona.

**Query Parameters:**
- `user_id` (string, optional): User ID, default "default"

**Response:**
```json
{
  "name": "MedRA",
  "role": "Medical Research Assistant",
  "tone": "professional, precise, and evidence-based",
  "expertise": [
    "medical literature review",
    "drug comparison",
    "clinical trial analysis"
  ],
  "greeting": "Hello! I'm MedRA...",
  "system_prompt_extra": ""
}
```

---

### PUT `/persona`
Update agent persona.

**Query Parameters:**
- `user_id` (string, optional): User ID, default "default"

**Request Body:**
```json
{
  "name": "Dr. Atlas",
  "tone": "friendly and educational",
  "expertise": ["oncology", "immunotherapy", "clinical trials"]
}
```

**Response:**
```json
{
  "name": "Dr. Atlas",
  "role": "Medical Research Assistant",
  "tone": "friendly and educational",
  "expertise": ["oncology", "immunotherapy", "clinical trials"],
  "greeting": "Hello! I'm MedRA...",
  "system_prompt_extra": ""
}
```

---

### GET `/profile`
Get user profile with interests and history.

**Query Parameters:**
- `user_id` (string, optional): User ID, default "default"

**Response:**
```json
{
  "user_id": "user123",
  "research_interests": ["diabetes", "oncology", "neurology"],
  "past_queries": [
    "What are the latest treatments for type 2 diabetes?",
    "Compare insulin types"
  ],
  "saved_papers": ["paper_id_1", "paper_id_2"],
  "preferences": {
    "detail_level": "advanced",
    "citation_style": "APA"
  },
  "created_at": "2024-01-15T10:30:00"
}
```

---

### POST `/interests`
Add research interest to profile.

**Request:**
```bash
curl -X POST http://localhost:8000/interests \
  -H "Content-Type: application/json" \
  -d '{
    "interest": "Parkinson'\''s disease",
    "user_id": "user123"
  }'
```

**Response:**
```json
{
  "status": "created",
  "interest": "Parkinson's disease"
}
```

---

### GET `/history`
Get conversation history and past queries.

**Query Parameters:**
- `user_id` (string, optional): User ID, default "default"

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What are pain management options for fibromyalgia?"
    },
    {
      "role": "assistant",
      "content": "## Fibromyalgia Pain Management\n\n..."
    }
  ],
  "past_queries": [
    "What is fibromyalgia?",
    "Latest fibromyalgia treatments",
    "Pain management for fibromyalgia?"
  ]
}
```

---

### POST `/history/clear`
Clear conversation history.

**Query Parameters:**
- `user_id` (string, optional): User ID, default "default"

**Response:**
```json
{
  "status": "cleared"
}
```

---

## Evaluation

### GET `/evaluation/stats`
Get aggregate evaluation statistics.

**Response:**
```json
{
  "total_evaluations": 42,
  "faithfulness": {
    "mean": 0.89,
    "min": 0.71,
    "max": 0.98
  },
  "answer_relevancy": {
    "mean": 0.85,
    "min": 0.68,
    "max": 0.96
  },
  "context_relevancy": {
    "mean": 0.87,
    "min": 0.74,
    "max": 0.97
  },
  "hallucination_score": {
    "mean": 0.18,
    "min": 0.05,
    "max": 0.42
  }
}
```

---

### POST `/evaluation/evaluate`
Evaluate a specific query (runs new evaluation).

**Request:**
```bash
curl -X POST http://localhost:8000/evaluation/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the pathophysiology of type 2 diabetes?",
    "user_id": "user123",
    "evaluate": true
  }'
```

**Response:**
```json
{
  "query": "What is the pathophysiology of type 2 diabetes?",
  "metrics": {
    "faithfulness": 0.93,
    "answer_relevancy": 0.89,
    "context_relevancy": 0.91,
    "hallucination_score": 0.08,
    "correctness": 0.91,
    "evaluation_notes": "High quality response with good source alignment"
  },
  "stats": {
    "total_evaluations": 43,
    "faithfulness": {
      "mean": 0.89,
      "min": 0.71,
      "max": 0.98
    }
  }
}
```

---

## Admin

### GET `/admin/sessions`
List all active user sessions.

**Response:**
```json
{
  "total_sessions": 3,
  "sessions": ["user123", "user456", "default"]
}
```

---

### POST `/admin/session/{user_id}/reset`
Reset a user's session.

**Path Parameters:**
- `user_id` (string, required): User ID to reset

**Response:**
```json
{
  "status": "reset"
}
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid input) |
| 404 | Not found |
| 500 | Server error (processing failed) |

---

## Rate Limiting

- Default: 100 requests/minute per user
- Query processing: 5-60 seconds depending on complexity

---

## Authentication

Currently no authentication. For production:

```env
# In .env
REQUIRE_AUTH=true
JWT_SECRET=your-secret-key
```

---

## Example Workflows

### Workflow 1: Simple Query

```bash
# 1. Submit query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest diabetes treatments"}'

# 2. Get results (includes evaluation)
# Response contains answer, sources, confidence
```

### Workflow 2: Build Custom Knowledge Base

```bash
# 1. Upload papers
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@paper1.pdf"
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@paper2.pdf"

# 2. Verify papers indexed
curl http://localhost:8000/knowledge-base/stats

# 3. Query with custom papers
curl -X POST http://localhost:8000/query \
  -d '{"query": "Findings from my papers"}'
```

### Workflow 3: Personalize Agent

```bash
# 1. Update persona
curl -X PUT http://localhost:8000/persona \
  -d '{
    "name": "Dr. Cancer Expert",
    "expertise": ["oncology", "immunotherapy"]
  }'

# 2. Add interests
curl -X POST http://localhost:8000/interests \
  -d '{"interest": "breast cancer"}'

# 3. Query with personalized agent
curl -X POST http://localhost:8000/query \
  -d '{"query": "New breast cancer treatments"}'
```

---

## Performance Tips

1. **Batch queries:** Use multiple `/query` calls sequentially, not parallel
2. **Cache results:** Store `/evaluation/stats` locally
3. **Monitor:** Check `execution_time_ms` in responses
4. **Optimize KB:** Keep knowledge base under 1000 papers for best performance

---

## Support

- Errors? Check `.env` configuration
- Slow responses? Reduce `RAG_TOP_K` in .env
- Memory issues? Clear old papers with `/knowledge-base/clear`

---

**API Version:** 2.0.0  
**Last Updated:** 2024  
**Status:** Production-Ready
