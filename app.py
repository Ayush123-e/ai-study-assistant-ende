import streamlit as st
from rag import rag_pipeline

st.set_page_config(
    page_title="AI Study Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium dark design with glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global reset */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 2rem 1rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.4rem 1rem;
        border-radius: 100px;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a5b4fc, #818cf8, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(199, 210, 254, 0.7);
        max-width: 500px;
        margin: 0 auto 2.5rem auto;
    }

    /* Search box area */
    .search-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(15, 12, 41, 0.8) !important;
        border: 1px solid rgba(165, 180, 252, 0.3) !important;
        border-radius: 12px !important;
        color: #e0e7ff !important;
        font-size: 1rem !important;
        padding: 0.85rem 1.2rem !important;
        transition: all 0.3s ease !important;
        caret-color: #a5b4fc !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(165, 180, 252, 0.8) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        background: rgba(30, 27, 75, 0.9) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(165, 180, 252, 0.45) !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6) !important;
    }

    /* Answer card */
    .answer-card {
        background: rgba(99, 102, 241, 0.08);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 1.8rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }

    .answer-label {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a5b4fc;
        margin-bottom: 0.8rem;
    }

    .answer-text {
        color: rgba(224, 231, 255, 0.95);
        font-size: 1rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }

    /* Document result cards */
    .doc-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .doc-card:hover {
        border-color: rgba(165, 180, 252, 0.3);
        background: rgba(255, 255, 255, 0.07);
        transform: translateX(4px);
    }

    .doc-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.8rem;
    }

    .doc-id {
        font-weight: 600;
        font-size: 0.9rem;
        color: #a5b4fc;
        background: rgba(99, 102, 241, 0.15);
        padding: 0.2rem 0.7rem;
        border-radius: 6px;
    }

    .score-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.7rem;
        border-radius: 100px;
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .score-badge.low {
        background: rgba(245, 158, 11, 0.1);
        color: #fcd34d;
        border-color: rgba(245, 158, 11, 0.3);
    }

    .doc-text {
        color: rgba(199, 210, 254, 0.7);
        font-size: 0.9rem;
        line-height: 1.7;
    }

    /* Section labels */
    .section-label {
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(165, 180, 252, 0.6);
        margin: 1.5rem 0 0.8rem 0;
    }

    /* Topics bar */
    .topics-bar {
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .topic-chip {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: rgba(199, 210, 254, 0.8);
        padding: 0.35rem 0.9rem;
        border-radius: 100px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Hide streamlit elements */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; }

    /* Warning */
    .stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

#  Hero 
st.markdown("""
<div class="hero-container">
    <div class="hero-badge"> Powered by Endee Vector DB</div>
    <div class="hero-title">AI Study Assistant</div>
    <div class="hero-subtitle">Ask anything about AI, Machine Learning, DevOps, and Data Science — powered by semantic search.</div>
    <div class="topics-bar">
        <span class="topic-chip"> Artificial Intelligence</span>
        <span class="topic-chip"> Machine Learning</span>
        <span class="topic-chip"> Data Science</span>
        <span class="topic-chip"> DevOps</span>
    </div>
</div>
""", unsafe_allow_html=True)

#  Search Box 
col_left, col_center, col_right = st.columns([1, 3, 1])
with col_center:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    query = st.text_input(
        label="",
        placeholder="e.g. What is supervised learning?",
        label_visibility="collapsed",
        key="query_input"
    )
    search_clicked = st.button("  Search Knowledge Base")
    st.markdown('</div>', unsafe_allow_html=True)

#  Results 
GREETINGS = {"hi", "hello", "hey", "hii", "ok", "okay", "yo", "sup", "bye", "thanks", "lol"}

def is_meaningful_query(q: str) -> tuple[bool, str]:
    q = q.strip()
    words = q.lower().split()
    word_set = set(words)

    if len(q) < 5:
        return False, "Your question is too short. Try something like *'What is machine learning?'*"
    if word_set.issubset(GREETINGS):
        return False, "I'm a study assistant, not a chatbot! Ask me a topic question. "
    if len(words) < 3 and "?" not in q:
        return False, "Please ask a clearer question (e.g. *'Explain DevOps'* or *'What is AI?'*)."
    return True, ""

if search_clicked:
    if not query.strip():
        st.warning("Please enter a question to search.")
    else:
        valid, reason = is_meaningful_query(query)
        if not valid:
            col_left, col_warn, col_right = st.columns([1, 3, 1])
            with col_warn:
                st.markdown(f"""
                <div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
                border-radius:14px;padding:1.2rem 1.5rem;color:#fca5a5;font-size:0.95rem;">
                     &nbsp;{reason}
                </div>
                """, unsafe_allow_html=True)
        else:
            with st.spinner("Searching knowledge base..."):
                answer, results = rag_pipeline(query)

            col_left, col_main, col_right = st.columns([1, 3, 1])
            with col_main:

                #  Answer Card 
                st.markdown(f"""
                <div class="answer-card">
                    <div class="answer-label"> Answer</div>
                    <div class="answer-text">{answer}</div>
                </div>
                """, unsafe_allow_html=True)

                #  Top Documents 
                if results:
                    st.markdown('<div class="section-label"> Top Retrieved Documents</div>', unsafe_allow_html=True)

                    for r in results:
                        doc_id = r.get("id", "unknown")
                        score = r.get("score", 0)
                        text = r.get("metadata", {}).get("text", "")
                        score_class = "low" if score < 0.4 else ""
                        preview = text[:280] + "..." if len(text) > 280 else text

                        st.markdown(f"""
                        <div class="doc-card">
                            <div class="doc-header">
                                <span class="doc-id"> {doc_id}</span>
                                <span class="score-badge {score_class}">Score: {score:.4f}</span>
                            </div>
                            <div class="doc-text">{preview}</div>
                        </div>
                        """, unsafe_allow_html=True)
