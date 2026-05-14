import requests
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Drive Agent",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0f172a 0%, #050816 55%);
    color: white;
}

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* NAVBAR */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.logo {
    font-size: 1.4rem;
    font-weight: 700;
    color: white;
}

.right-nav {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: #9ca3af;
}

.online {
    color: #22c55e;
}

/* HERO */

.hero {
    text-align: center;
    margin-top: 3rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 4.2rem;
    font-weight: 800;
    background: linear-gradient(90deg,#a855f7,#60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #9ca3af;
    font-size: 1.1rem;
    margin-top: 1rem;
}

/* SECTION */

.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

/* QUICK SEARCH */

.tip-btn button {
    background: rgba(17,24,39,0.8) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 18px !important;
    padding: 1rem !important;
    width: 100% !important;
    text-align: center !important;
    height: 70px !important;
    color: white !important;
    transition: 0.3s !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

.tip-btn button:hover {
    border: 1px solid #8b5cf6 !important;
    transform: translateY(-2px);
}

/* RESULT CARD */

.result-card {
    background: rgba(17,24,39,0.75);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.2rem;
    margin-top: 1rem;
}

.file-title {
    font-size: 1.1rem;
    font-weight: 600;
}

.file-meta {
    color: #9ca3af;
    margin-top: 0.4rem;
}

.open-btn {
    display: inline-block;
    margin-top: 1rem;
    background: linear-gradient(90deg,#8b5cf6,#3b82f6);
    padding: 0.6rem 1rem;
    border-radius: 10px;
    color: white !important;
    text-decoration: none;
    font-weight: 600;
}

/* CHAT INPUT */

.stChatInputContainer {
    background: rgba(17,24,39,0.85) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 18px !important;
}

/* MOBILE */

@media(max-width: 900px) {

    .hero-title {
        font-size: 3rem;
    }
}

@media(max-width: 600px) {

    .hero-title {
        font-size: 2.2rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# NAVBAR
# ---------------------------------------------------------

st.markdown("""
<div class="topbar">

<div class="logo">
📁 AI Drive Agent
</div>

<div class="right-nav">
ℹ️ About
<span class="online">● Online</span>
</div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
✨ AI Google Drive Agent
</div>

<div class="hero-subtitle">
Conversational AI system for intelligent file discovery and semantic Google Drive search.
</div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "current_search" not in st.session_state:
    st.session_state.current_search = None

# ---------------------------------------------------------
# QUICK SEARCHES
# ---------------------------------------------------------

quick_queries = [
    ("📄 Find PDFs", "Find PDF reports"),
    ("🖼️ Find Images", "Show image files"),
    ("🧾 Find Invoices", "Find invoice documents"),
    ("📊 Find Reports", "Find report files")
]

selected_query = None

st.markdown("""
<div class="section-title">
💡 Quick Searches
</div>
""", unsafe_allow_html=True)

cols = st.columns(4)

for i, (title, query_text) in enumerate(quick_queries):

    with cols[i]:

        st.markdown(
            '<div class="tip-btn">',
            unsafe_allow_html=True
        )

        if st.button(title, key=query_text):
            selected_query = query_text

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_input = st.chat_input(
    "Ask about your Google Drive files..."
)

if selected_query:
    user_input = selected_query

# ---------------------------------------------------------
# API REQUEST
# ---------------------------------------------------------

if user_input:

    with st.spinner("Thinking..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": user_input
                }
            )

            data = response.json()

            reply = data.get("reply", "")
            results = data.get("results", [])
            is_search = data.get("is_search", False)

            search_data = {
                "question": user_input,
                "reply": reply,
                "results": results,
                "is_search": is_search
            }

            # SAVE OLD CHAT TO HISTORY

            if st.session_state.current_search is not None:

                st.session_state.history.insert(
                    0,
                    st.session_state.current_search
                )

            # SAVE CURRENT CHAT

            st.session_state.current_search = search_data

        except Exception as e:

            st.error(str(e))

# ---------------------------------------------------------
# CURRENT CHAT
# ---------------------------------------------------------

if st.session_state.current_search:

    item = st.session_state.current_search

    st.markdown("""
<div class="section-title">
✨ Latest Chat
</div>
""", unsafe_allow_html=True)

    # USER MESSAGE

    st.markdown(f"""
<div style="
display:flex;
justify-content:flex-end;
margin-bottom:14px;
">

<div style="
background:linear-gradient(90deg,#8b5cf6,#3b82f6);
padding:14px 18px;
border-radius:18px 18px 4px 18px;
max-width:70%;
font-size:16px;
font-weight:500;
color:white;
box-shadow:0 0 20px rgba(139,92,246,0.2);
">

{item['question']}

</div>

</div>
""", unsafe_allow_html=True)

    # AI RESPONSE

    st.markdown(f"""
<div style="
display:flex;
justify-content:flex-start;
margin-bottom:18px;
">

<div style="
background:rgba(17,24,39,0.85);
border:1px solid rgba(255,255,255,0.06);
padding:16px 18px;
border-radius:18px 18px 18px 4px;
max-width:75%;
font-size:16px;
line-height:1.7;
color:#d1d5db;
">

🤖 {item['reply']}

</div>

</div>
""", unsafe_allow_html=True)

    # FILE RESULTS

    if item["is_search"]:

        results = item["results"]

        if len(results) == 0:

            st.warning(
                "No matching files found."
            )

        else:

            st.markdown("""
<div class="section-title">
📂 Matching Files
</div>
""", unsafe_allow_html=True)

            for file in results:

                st.markdown(f"""
<div class="result-card">

<div class="file-title">
📄 {file['name']}
</div>

<div class="file-meta">
<b>Type:</b> {file['mimeType']}
</div>

<div class="file-meta">
<b>Modified:</b> {file['modifiedTime']}
</div>

<a class="open-btn"
href="{file['webViewLink']}"
target="_blank">
Open File
</a>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------

if st.session_state.history:

    with st.expander("🕘 Chat History"):

        for item in st.session_state.history:

            # USER

            st.markdown(f"""
<div style="
display:flex;
justify-content:flex-end;
margin-bottom:10px;
">

<div style="
background:linear-gradient(90deg,#8b5cf6,#3b82f6);
padding:12px 16px;
border-radius:18px 18px 4px 18px;
max-width:70%;
color:white;
">

{item['question']}

</div>

</div>
""", unsafe_allow_html=True)

            # BOT

            st.markdown(f"""
<div style="
display:flex;
justify-content:flex-start;
margin-bottom:18px;
">

<div style="
background:rgba(17,24,39,0.85);
border:1px solid rgba(255,255,255,0.06);
padding:14px 16px;
border-radius:18px 18px 18px 4px;
max-width:75%;
color:#d1d5db;
">

🤖 {item['reply']}

</div>

</div>
""", unsafe_allow_html=True)