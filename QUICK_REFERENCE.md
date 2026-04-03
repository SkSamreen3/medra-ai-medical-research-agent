# MedRA v2.0 — QUICK REFERENCE GUIDE

## 🚀 Start in 30 Seconds

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env: add OPENAI_API_KEY

# 3. Run
uvicorn app.main:app --reload

# 4. Test (new terminal)
curl http://localhost:8000/

# 5. Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "diabetes treatment options"}'
```

---

## 📁 Project Structure

```
agentic_ai_lab05/
├── app/
│   ├── main.py           # FastAPI app (enhanced)
│   ├── agents.py         # 5-agent orchestration (NEW)
│   ├── rag.py            # ChromaDB pipeline
│   ├── config.py         # Configuration (50+ settings)
│   ├── models.py         # Data models (+ evaluation)
│   ├── memory.py         # Memory management (+ vector)
│   ├── tools.py          # PubMed, arXiv, PDF parsing
│   ├── evaluation.py     # RAGAS framework (NEW)
│   └── __init__.py
├── ui.py                 # Streamlit UI
├── requirements.txt      # Dependencies (40+ new)
├── .env.example          # Configuration template
├── Dockerfile            # Docker image
├── docker-compose.yml    # Multi-container setup
├── README.md             # Project overview
├── UPGRADE.md            # Migration guide
├── API.md                # API documentation
└── TRANSFORMATION_SUMMARY.md  # This file
```

---

## 🤖 System Architecture

```
User Query
    ↓
┌─────────────────────┐
│ FastAPI Backend     │ (Enhanced v2.0)
└──────────┬──────────┘
           ↓
┌─────────────────────────────────────────┐
│  LangGraph Multi-Agent Orchestrator     │
│                                          │
│  [Research] → [Summarizer] → [Analyst]  │
│      ↓            ↓              ↓       │
│  [Papers]    [Findings]    [Comparison] │
│      ↓            ↓              ↓       │
│    ├────────────[Critic Agent]─────╮   │
│    │          (Verify)             │   │
│    └────────────[Memory Agent]─────╯   │
└──────────────────┬────────────────────┘
                   ↓
        ┌─────────────────────┐
        │ ChromaDB RAG        │
        │ + Hybrid Search     │
        │ + Reranking         │
        └──────────┬──────────┘
                   ↓
        ┌─────────────────────┐
        │ RAGAS Evaluation    │ (Quality metrics)
        └─────────────────────┘
                   ↓
        ┌─────────────────────┐
        │ Structured Response │ (JSON + metrics)
        └─────────────────────┘
```

---

## 5️⃣ The Five Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| 🔍 **Research** | Find papers | Query | Papers[] |
| 📄 **Summarizer** | Extract info | Papers[] | Findings{} |
| 💊 **Analyst** | Medical analysis | Findings + Papers | Comparisons{} |
| ✓ **Critic** | Verify claims | Answer + Papers | Metrics{} |
| 🧠 **Memory** | Store insights | Insights + Tags | Stored |

---

## 🔧 Key Configuration

### Minimal (.env)
```env
# Required
OPENAI_API_KEY=sk-...

# Optional (has defaults)
OPENAI_MODEL=gpt-4o
ENABLE_EVALUATION=true
```

### Advanced Options
```env
# LLM switching
LLM_PROVIDER=openai                    # openai|anthropic
OPENAI_MODEL=gpt-4o
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet...

# Embeddings
EMBEDDING_PROVIDER=openai              # openai|huggingface
EMBEDDING_MODEL=text-embedding-3-large

# RAG tuning
RAG_TOP_K=10
RAG_USE_HYBRID_SEARCH=true
RAG_USE_RERANKER=true
RAG_CHUNK_SIZE=512

# Vector DB
CHROMA_PERSIST_DIR=./data/chroma_db

# Evaluation
ENABLE_EVALUATION=true
LANGSMITH_ENABLED=false
```

---

## 📡 API Endpoints (Main)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Health check |
| `POST` | `/query` | **Submit research question** |
| `POST` | `/upload-pdf` | Add paper to KB |
| `GET` | `/knowledge-base/stats` | KB info |
| `GET/PUT` | `/persona` | Customize agent |
| `GET` | `/evaluation/stats` | Quality metrics |

**Full API docs:** See `API.md`

---

## 💾 Data Storage

```
data/
├── chroma_db/          # Vector database (persistent)
│   ├── chroma.sqlite3  # ChromaDB index
│   └── embedding_fn_... # Serialized embeddings
├── papers/             # Uploaded PDFs
├── memory/             # User profiles & history
│   ├── profile_*.json  # Long-term profile
│   └── vector_memory_*.jsonl  # Semantic memories
└── evaluations/        # Evaluation results
    └── evaluations.jsonl     # Quality metrics history
```

---

## 📊 Response Structure

```json
{
  "answer": "Main response text",
  "reasoning_steps": [
    {
      "thought": "What the agent thought",
      "action": "What action it took",
      "observation": "What it discovered",
      "agent": "research|summarizer|critic|analyzer|memory"
    }
  ],
  "papers_used": [...],
  "sources": [...],
  "confidence": 0.92,
  "evaluation": {
    "faithfulness": 0.95,
    "answer_relevancy": 0.88,
    "hallucination_score": 0.12
  },
  "treatments_found": [...],
  "key_findings": [...],
  "execution_time_ms": 3245.5
}
```

---

## 🧪 Testing Checklist

```bash
# 1. Health
curl http://localhost:8000/

# 2. Upload PDF
curl -X POST http://localhost:8000/upload-pdf \
  -F "file=@test.pdf"

# 3. Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# 4. Evaluation stats
curl http://localhost:8000/evaluation/stats

# 5. Persona
curl http://localhost:8000/persona
```

---

## 🐳 Docker Deployment

```bash
# Build & run
docker compose up --build

# Services:
# - medra-api:8000         FastAPI
# - medra-chroma:8001      ChromaDB
# - medra-ui:8501          Streamlit
```

---

## 🔍 Vector DB Comparison

| Feature | FAISS (Old) | ChromaDB (New) |
|---------|------------|--------|
| Persistence | File-based | Embedded DB |
| Scaling | Limited | Excellent |
| Querying | Slow | Fast + filtering |
| Metadata | Limited | Full support |
| Updates | Rebuild needed | Online |
| Production | ❌ Risky | ✅ Recommended |

---

## 📈 Evaluation Metrics

Each response includes:

| Metric | Range | Meaning |
|--------|-------|---------|
| **Faithfulness** | 0-1 | Truth of answer vs sources |
| **Answer Relevancy** | 0-1 | Relevance to query |
| **Context Relevancy** | 0-1 | Quality of retrieved docs |
| **Hallucination Score** | 0-1 | Probability of hallucination |
| **Correctness** | 0-1 | Overall accuracy |

---

## 🆘 Common Issues & Fixes

### Issue: ModuleNotFoundError
```bash
# Fix: Install dependencies
pip install -r requirements.txt
```

### Issue: OPENAI_API_KEY not found
```bash
# Fix: Create .env file
cp .env.example .env
# Edit and add your key
```

### Issue: ChromaDB connection failed
```bash
# Fix: Delete and reset
rm -rf ./data/chroma_db
# Restart app
```

### Issue: Slow queries
```env
# Fix: Reduce results
RAG_TOP_K=5
RAG_USE_RERANKER=false
```

---

## 🚀 Performance Tips

1. **Parallel Processing:** Research Agent queries PubMed + arXiv simultaneously
2. **Caching:** Agent decisions cached per session
3. **Streaming:** Large responses can be streamed
4. **Batching:** Group multiple queries before evaluation

---

## 📚 Documentation Map

| Document | Content |
|----------|---------|
| README.md | Project overview & features |
| UPGRADE.md | Migration from v1.0 |
| TRANSFORMATION_SUMMARY.md | **What changed** |
| API.md | Endpoint documentation |
| This file | Quick reference |

---

## 🎯 Next Steps

1. ✅ **Install:** `pip install -r requirements.txt`
2. ✅ **Configure:** Add API keys to `.env`
3. ✅ **Run:** `uvicorn app.main:app --reload`
4. ✅ **Test:** Various queries
5. ✅ **Deploy:** `docker compose up`
6. ✅ **Monitor:** Check evaluation stats

---

## 💡 Pro Tips

- **Hybrid Search:** Better than pure semantic (set `RAG_USE_HYBRID_SEARCH=true`)
- **Reranking:** Improves top results significantly
- **Evaluation:** Always enable in production
- **LangSmith:** Optional monitoring at scale
- **Custom KB:** Upload papers relevant to your domain

---

## 🔗 External Resources

- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [RAGAS Framework](https://docs.ragas.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)

---

**Last Updated:** 2024  
**Version:** 2.0.0  
**Status:** ✅ Production-Ready
