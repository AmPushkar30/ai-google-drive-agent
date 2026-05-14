import streamlit as st
import requests
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Google Drive Agent",
    page_icon="✨",
    layout="wide"
)

# =========================
# BACKEND URL
# =========================

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://ai-google-drive-agent.onrender.com"
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #020617;
    color: white;
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Branding */

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Layout */

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

/* Hero Section */

.hero-title {
    font-size: 72px;
    font-weight: 800;
    text-align: center;
    line-height: 1.1;
    background: linear-gradient(90deg,#a855f7,#60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    text-align: center;
    color: #94a3b8;
    font-size: 22px;
    margin-top: 15px;
    margin-bottom: 60px;
}

/* Quick Search */

.quick-title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* User Bubble */

.user-wrap {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
    margin-bottom: 15px;
}

.user-bubble {
    background: linear-gradient(135deg,#a855f7,#3b82f6);
    padding: 18px 22px;
    border-radius: 20px;
    color: white;
    max-width: 420px;
    font-size: 17px;
    font-weight: 500;
}

/* AI Bubble */

.ai-wrap {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 20px;
}

.ai-bubble {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 18px 22px;
    border-radius: 20px;
    color: white;
    max-width: 650px;
    font-size: 17px;
    line-height: 1.6;
}

/* File Cards */

.file-card {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 28px;
    margin-top: 15px;
    margin-bottom: 20px;
}

.file-name {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 14px;
}

.file-meta {
    color: #94a3b8;
    margin-bottom: 10px;
    font-size: 16px;
}

.open-btn {
    display: inline-block;
    padding: 12px 20px;
    border-radius: 14px;
    background: linear-gradient(135deg,#a855f7,#3b82f6);
    color: white !important;
    text-decoration: none;
    font-weight: 600;
    margin-top: 12px;
}

/* Input */

.stChatInputContainer {
    background: #020617;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div style="text-align:center; margin-top:30px;">
    <div class="hero-title">✨ AI Google Drive Agent</div>

    <div class="hero-sub">
        Conversational AI system for intelligent file discovery and semantic Google Drive search.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# QUICK SEARCH
# =========================

st.markdown(
    '<div class="quick-title">💡 Quick Searches</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("📄 Find PDFs", use_container_width=True):
        query = "find pdf files"

with c2:
    if st.button("🖼️ Find Images", use_container_width=True):
        query = "find images"

with c3:
    if st.button("🧾 Find Invoices", use_container_width=True):
        query = "find invoices"

with c4:
    if st.button("📊 Find Reports", use_container_width=True):
        query = "find reports"

# =========================
# CHAT INPUT
# =========================

user_input = st.chat_input("Ask about your Google Drive files...")

if user_input:
    query = user_input

# =========================
# SEND REQUEST
# =========================

if "query" in locals():

    try:

        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": query}
        )

        data = response.json()

        st.session_state.messages.append({
            "user": query,
            "reply": data.get("reply", ""),
            "results": data.get("results", [])
        })

    except Exception as e:

        st.session_state.messages.append({
            "user": query,
            "reply": f"Error: {str(e)}",
            "results": []
        })

# =========================
# CHAT DISPLAY
# =========================

for msg in st.session_state.messages:

    # USER MESSAGE

    st.markdown(f"""
    <div class="user-wrap">
        <div class="user-bubble">
            {msg["user"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI MESSAGE

    st.markdown(f"""
    <div class="ai-wrap">
        <div class="ai-bubble">
            🤖 {msg["reply"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # FILE RESULTS

    if msg["results"]:

        for file in msg["results"]:

            file_name = file.get("name", "Unknown File")
            file_type = file.get("mimeType", "Unknown")
            modified = file.get("modifiedTime", "")
            link = file.get("webViewLink", "#")

            file_html = f"""
            <div class="file-card">

                <div class="file-name">
                    📄 {file_name}
                </div>

                <div class="file-meta">
                    Type: {file_type}
                </div>

                <div class="file-meta">
                    Modified: {modified}
                </div>

                <a class="open-btn"
                   href="{link}"
                   target="_blank">
                    Open File
                </a>

            </div>
            """

            st.markdown(file_html, unsafe_allow_html=True)