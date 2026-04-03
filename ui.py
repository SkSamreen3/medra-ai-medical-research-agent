"""Streamlit UI for MedRA - Medical Research Agent."""

import asyncio
import json
import logging
from typing import Optional

import streamlit as st

from app.config import settings
from app.models import AgentResult, Persona
from app.agents import MultiAgentOrchestrator
from app.memory import MemoryManager
from app import rag

logger = logging.getLogger(__name__)

# =====================================================================
# Streamlit Configuration 
# =====================================================================

st.set_page_config(
    page_title=settings.streamlit_page_title,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
    .info-box { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
    .warning-box { background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
    .success-box { background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# Session State 
# =====================================================================

if "user_id" not in st.session_state:
    st.session_state.user_id = "default"

if "memory" not in st.session_state:
    st.session_state.memory = MemoryManager(st.session_state.user_id)

if "persona" not in st.session_state:
    st.session_state.persona = Persona()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = MultiAgentOrchestrator(st.session_state.persona)


# =====================================================================
# Sidebar
# =====================================================================

with st.sidebar:
    st.title("⚙️ Configuration")

    st.session_state.user_id = st.text_input("User ID", st.session_state.user_id)

    st.divider()

    st.subheader("🎭 Agent Persona")
    st.session_state.persona.name = st.text_input("Name", st.session_state.persona.name)
    st.session_state.persona.tone = st.text_area("Tone", st.session_state.persona.tone, height=60)

    st.divider()

    st.subheader("📚 Knowledge Base")
    st.metric("Papers Indexed", rag.total_papers())
    if st.button("🗑️ Clear KB"):
        rag.clear_index()
        st.success("Cleared!")

    st.divider()

    with st.expander("⚠️ Medical Disclaimer"):
        st.markdown("""
        **Educational use only.** Not a replacement for professional medical advice.  
        Please consult a qualified healthcare provider.
        """)


# =====================================================================
# Main Content
# =====================================================================

st.title("🏥 MedRA — Medical Research Agent")
st.markdown("*Production-grade multi-agent medical research system*")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📤 Upload PDF", "👤 Profile"])

# =====================================================================
# TAB 1: Chat
# =====================================================================

with tab1:
    st.subheader("Ask a Research Question")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Clear"):
            st.session_state.messages = []
            st.success("Cleared!")

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask about medical research...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.memory.add_message("user", user_input)

        with st.spinner("🔬 Analyzing research..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                result = loop.run_until_complete(
                    st.session_state.orchestrator.run(user_input, st.session_state.user_id)
                )
                loop.close()

                st.session_state.memory.add_message("assistant", result.answer)

                with st.chat_message("assistant"):
                    st.markdown(result.answer)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Confidence", f"{result.confidence:.1%}")
                    with col2:
                        st.metric("Papers", len(result.papers_used))
                    with col3:
                        st.metric("Time (ms)", f"{result.execution_time_ms:.0f}")

                    if result.papers_used:
                        with st.expander("📚 Sources"):
                            for i, p in enumerate(result.papers_used[:5], 1):
                                st.markdown(f"**{i}. {p.title}**")
                                if p.doi:
                                    st.caption(f"[DOI: {p.doi}](https://doi.org/{p.doi})")

                    st.markdown(f"<div class='warning-box'><small>{result.medical_disclaimer}</small></div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


# =====================================================================
# TAB 2: Upload PDF
# =====================================================================

with tab2:
    st.subheader("📤 Upload Medical Papers")

    uploaded = st.file_uploader("Choose PDF", type=["pdf"])

    if uploaded and st.button("📥 Upload & Index"):
        with st.spinner("Processing..."):
            try:
                from app import tools
                
                content = uploaded.read()
                paper = tools.parse_pdf_bytes(content, uploaded.name)
                rag.add_papers([paper])
                
                st.success(f"✅ Indexed! Total: {rag.total_papers()}")
            except Exception as e:
                st.error(f"Failed: {str(e)}")


# =====================================================================
# TAB 3: Profile
# =====================================================================

with tab3:
    st.subheader("👤 User Profile")
    
    profile = st.session_state.memory.profile
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Past Queries", len(profile.past_queries))
    with col2:
        st.metric("Saved Papers", len(profile.saved_papers))


st.divider()
st.markdown("<small>MedRA v2.0 | LangGraph + ChromaDB + OpenAI</small>", unsafe_allow_html=True)
