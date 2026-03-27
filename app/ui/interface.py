import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from app.core.security import authenticate_user, redact_pii
from app.core.chain import build_chain

# --- Page config ---
st.set_page_config(
    page_title="Secure Clinical RAG Engine",
    page_icon="🏥",
    layout="wide"
)

# --- Custom styling ---
st.markdown("""
    <style>
        .role-badge {
            background-color: #E1F5EE;
            color: #085041;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
        }
        .source-box {
            background-color: #f8f9fa;
            border-left: 3px solid #1D9E75;
            padding: 8px 12px;
            margin: 4px 0;
            border-radius: 0 8px 8px 0;
            font-size: 13px;
            color: #444;
        }
    </style>
""", unsafe_allow_html=True)

# --- Session state setup ---
# Session state is like short-term memory for the app
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chain" not in st.session_state:
    st.session_state.chain = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# =====================
# LOGIN PAGE
# =====================
def show_login():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🏥 Clinical RAG Engine")
        st.markdown("#### Secure Document Intelligence")
        st.divider()

        with st.container(border=True):
            st.markdown("##### Sign in to continue")
            username = st.text_input("Username", placeholder="e.g. dr_smith")
            password = st.text_input("Password", type="password")
            login_btn = st.button("Sign In", use_container_width=True, type="primary")

            if login_btn:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    # Build the chain for this user's role
                    with st.spinner("Loading your documents..."):
                        chain, retriever = build_chain(role=user["role"])
                        st.session_state.chain = chain
                        st.session_state.retriever = retriever
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        st.divider()
        st.markdown("**Demo accounts:**")
        demo_data = {
            "Username": ["dr_smith", "analyst_jane", "hr_bob", "admin_root"],
            "Password": ["clinic123", "data456", "hr789", "admin000"],
            "Role": ["clinician", "informatics", "hr", "admin"]
        }
        st.dataframe(demo_data, use_container_width=True, hide_index=True)

# =====================
# CHAT PAGE
# =====================
def show_chat():
    user = st.session_state.user

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🏥 Clinical RAG Engine")
    with col2:
        st.markdown(f"""
            <div style='text-align:right; padding-top: 16px;'>
                <span class='role-badge'>{user['role']}: {user['username']}</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.chat_history = []
            st.session_state.chain = None
            st.rerun()

    st.divider()

    # Two column layout: chat on left, info on right
    chat_col, info_col = st.columns([2, 1])

    with info_col:
        with st.container(border=True):
            st.markdown("##### Your access level")
            from app.core.security import ROLE_PERMISSIONS
            allowed = ROLE_PERMISSIONS.get(user["role"], [])
            for category in allowed:
                st.markdown(f"- {category}")
        st.markdown(" ")
        with st.container(border=True):
            st.markdown("##### How to use")
            st.markdown("""
                1. Type a question below
                2. The AI searches only your allowed documents
                3. All PII is automatically redacted
                4. Sources are shown with every answer
            """)

    with chat_col:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("View sources"):
                        for src in message["sources"]:
                            st.markdown(f"""
                                <div class='source-box'>
                                    {redact_pii(src[:400])}...
                                </div>
                            """, unsafe_allow_html=True)

        # Chat input
        question = st.chat_input("Ask a question about your documents...")
        if question:
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })

            # Get answer from chain
            with st.spinner("Searching documents..."):
                answer = st.session_state.chain.invoke(question)
                sources = st.session_state.retriever.invoke(question)
                source_texts = [doc.page_content for doc in sources]

            # Add AI response to history
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer,
                "sources": source_texts
            })

            st.rerun()

# =====================
# MAIN APP ROUTER
# =====================
if st.session_state.logged_in:
    show_chat()
else:
    show_login()