import os
import streamlit as st
from streamlit_chat import message
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="ByteBuddy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- theme ----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def set_theme(theme: str):
    st.session_state.theme = theme
    st.rerun()

light_theme = """
<style>
    :root {
        --bg: #f4f7fb;
        --panel: rgba(255,255,255,0.8);
        --panel-strong: #ffffff;
        --card: #ffffff;
        --ink: #101828;
        --muted: #667085;
        --line: rgba(16,24,40,0.08);
        --primary: #5b5cf6;
        --primary-soft: #eef0ff;
        --accent: #11b981;
        --shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
    }
    .stApp {
        background: linear-gradient(180deg, #f7f9ff 0%, #eef3ff 100%);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(12px);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }
    .glass-card {
        background: rgba(255,255,255,0.7);
        border: 1px solid var(--line);
        border-radius: 20px;
        box-shadow: var(--shadow);
        padding: 1.5rem;
        backdrop-filter: blur(12px);
    }
    .hero-badge {
        display: inline-block;
        background: var(--primary-soft);
        color: var(--primary);
        border: 1px solid rgba(91,92,246,0.12);
        border-radius: 999px;
        padding: 0.35rem 0.7rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .hero-title {
        font-size: clamp(2.2rem, 5vw, 4rem);
        line-height: 1.05;
        letter-spacing: -0.06em;
        margin: 0;
        font-weight: 800;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--muted);
        max-width: 700px;
    }
    .metric-box {
        background: var(--panel-strong);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: var(--shadow);
    }
    .metric-box strong {
        font-size: 1.4rem;
        color: var(--ink);
    }
    .chat-message {
        border-radius: 16px;
        border: 1px solid var(--line);
        background: rgba(255,255,255,0.9);
    }
</style>
"""

dark_theme = """
<style>
    .stApp {
        background: #0b1020;
        color: #e5e7eb;
    }
    [data-testid="stSidebar"] {
        background: rgba(12,17,28,0.9);
    }
    .glass-card, .metric-box {
        background: rgba(17,24,39,0.9);
        color: #edf2ff;
        border: 1px solid rgba(148,163,184,0.18);
    }
    .hero-subtitle, .metric-box p {
        color: #a5b4cf;
    }
    .stChatMessage {
        background: rgba(15, 23, 42, 0.95);
        color: #edf2ff;
    }
    .chat-message {
        background: rgba(15,23,42,0.96);
    }
</style>
"""

if st.session_state.theme == "light":
    st.markdown(light_theme, unsafe_allow_html=True)
else:
    st.markdown(dark_theme, unsafe_allow_html=True)

# ---------- session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "hf_token" not in st.session_state:
    st.session_state.hf_token = os.getenv("HF_TOKEN", "")

# ---------- sidebar ----------
with st.sidebar:
    st.markdown("### ⚙️ Workspace")
    st.caption("Run private AI chat locally with open-source models.")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("☀️ Light", use_container_width=True):
            set_theme("light")
    with col2:
        if st.button("🌙 Dark", use_container_width=True):
            set_theme("dark")

    st.divider()

    st.text_input(
        "Hugging Face Token",
        value=st.session_state.hf_token,
        type="password",
        help="Get your token from https://huggingface.co/settings/tokens",
        key="hf_token_input"
    )
    st.session_state.hf_token = st.session_state.hf_token_input

    model = st.selectbox(
        "Model",
        [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "meta-llama/Llama-2-7b-chat-hf",
            "HuggingFaceH4/zephyr-7b-beta",
            "tiiuae/falcon-7b-instruct",
        ],
        index=0,
    )

    temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Response Length", 50, 1024, 256, 50)
    top_p = st.slider("Top P", 0.0, 1.0, 0.95, 0.05)

    st.divider()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.info(f"Messages: {len(st.session_state.messages)}")

# ---------- hero ----------
st.markdown("""
<div class="glass-card">
    <div class="hero-badge">ByteBuddy • Local AI Studio</div>
    <h1 class="hero-title">Ship smarter ideas with a private AI assistant.</h1>
    <p class="hero-subtitle">
        ByteBuddy helps founders, builders, and teams prototype faster with open-source models,
        secure local workflows, and a clean chat experience built for daily use.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="metric-box">
        <p>⚡</p>
        <strong>5x</strong>
        <p>Faster idea iteration</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-box">
        <p>🔒</p>
        <strong>100%</strong>
        <p>Local-first workflow</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-box">
        <p>🤖</p>
        <strong>4</strong>
        <p>Open-source models</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- chat area ----------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

user_input = st.chat_input(
    "Ask ByteBuddy anything...",
    placeholder="Type a prompt and hit enter",
    disabled=not st.session_state.hf_token,
)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        with st.spinner("Thinking..."):
            client = InferenceClient(model=model, token=st.session_state.hf_token)
            prompt = ""
            for msg in st.session_state.messages[:-1]:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
            prompt += f"User: {user_input}\nAssistant:"
            response = client.text_generation(
                prompt=prompt,
                temperature=temperature,
                max_new_tokens=max_tokens,
                top_p=top_p,
            )
        assistant = response.strip()
        st.session_state.messages.append({"role": "assistant", "content": assistant})
        st.chat_message("assistant").write(assistant)
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
