import html
import streamlit as st
from markdown_it import MarkdownIt
from chatbot import get_response

# Initialize markdown parser for assistant messages (with table support)
md = MarkdownIt("commonmark").enable("table").enable("strikethrough")

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Surat Metro Chat",
    page_icon="🚇",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM STYLES (Compact Floating Card Widget Theme) ----------
st.markdown("""
<style>
    /* 1. Global Page Background (Light Grey as requested) */
    .stApp {
        background-color: #eef1f4 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* 2. Hide default Streamlit clutter */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    footer {
        display: none !important;
    }
    #MainMenu {
        display: none !important;
    }

    /* 3. Centered Compact Card Layout (Max-width ~360-380px) */
    .block-container {
        max-width: 380px !important;
        width: 100% !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5.5rem !important;
        margin: 0 auto !important;
    }

    /* Card Shell Wrapper */
    .widget-container {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
        border: 1px solid #e5e7eb;
        overflow: hidden;
        margin-bottom: 12px;
    }

    /* Header Section */
    .widget-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        background: #ffffff;
        border-bottom: 1px solid #f1f3f5;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .back-btn {
        color: #4b5563;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        padding-right: 2px;
    }
    .avatar-cluster {
        display: flex;
        align-items: center;
        position: relative;
        width: 38px;
        height: 28px;
    }
    .avatar-icon-1 {
        position: absolute;
        left: 0;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #7c3aed;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        border: 2px solid #ffffff;
        z-index: 2;
    }
    .avatar-icon-2 {
        position: absolute;
        left: 14px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #0284c7;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        border: 2px solid #ffffff;
        z-index: 1;
    }
    .header-info {
        display: flex;
        flex-direction: column;
    }
    .header-title {
        font-size: 14px;
        font-weight: 700;
        color: #111827;
        margin: 0;
        line-height: 1.2;
    }
    .header-subtitle {
        font-size: 11px;
        color: #6b7280;
        margin: 2px 0 0 0;
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .header-right {
        color: #9ca3af;
        font-size: 14px;
        cursor: pointer;
    }

    /* Welcome text banner */
    .welcome-text {
        text-align: center;
        padding: 10px 14px 4px 14px;
        font-size: 12px;
        color: #9ca3af;
        font-weight: 500;
        letter-spacing: -0.01em;
    }

    /* Message Rows & Bubbles */
    .chat-bubble-area {
        padding: 6px 14px 14px 14px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    /* Bot Greeting & Assistant Messages */
    .bot-row {
        display: flex;
        justify-content: flex-start;
        margin: 4px 0;
    }
    .bot-bubble {
        background-color: #f3f4f6;
        color: #1f2937;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 4px; /* chat tail effect */
        max-width: 85%;
        font-size: 13.5px;
        line-height: 1.5;
        word-break: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .bot-bubble p {
        margin: 0 0 6px 0;
    }
    .bot-bubble p:last-child {
        margin-bottom: 0;
    }
    .bot-bubble strong {
        color: #111827;
    }
    .bot-bubble ul, .bot-bubble ol {
        margin: 4px 0 6px 0;
        padding-left: 18px;
    }
    .bot-bubble li {
        margin-bottom: 2px;
    }
    .bot-bubble table {
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0;
        font-size: 12px;
        background: #ffffff;
        border-radius: 6px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    .bot-bubble th {
        background: #f9fafb;
        color: #111827;
        font-weight: 600;
        padding: 5px 8px;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
    }
    .bot-bubble td {
        padding: 5px 8px;
        border-bottom: 1px solid #f3f4f6;
        color: #374151;
    }

    /* User Message Bubble */
    .user-row {
        display: flex;
        justify-content: flex-end;
        margin: 4px 0;
    }
    .user-bubble {
        background-color: #7c3aed !important; /* Requested purple */
        color: #ffffff !important;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px; /* chat tail effect */
        max-width: 85%;
        font-size: 13.5px;
        line-height: 1.5;
        word-break: break-word;
        box-shadow: 0 2px 6px rgba(124, 58, 237, 0.25);
        font-weight: 450;
    }

    /* Quick Reply Pill Buttons */
    div.stButton {
        display: flex;
        justify-content: flex-end;
        margin-bottom: -6px;
    }
    div.stButton > button {
        background-color: #ffffff !important;
        color: #047857 !important; /* Greenish text like image */
        border: 1px solid #e5e7eb !important;
        border-radius: 20px !important;
        padding: 5px 14px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.15s ease-in-out !important;
        margin-left: auto !important;
        display: inline-block !important;
        width: auto !important;
    }
    div.stButton > button:hover {
        border-color: #7c3aed !important;
        color: #7c3aed !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.18) !important;
        transform: translateY(-1px) !important;
    }
    div.stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Streamlit Chat Input Styling (Bottom Fixed Pill) */
    div[data-testid="stBottom"] {
        background: transparent !important;
    }
    div[data-testid="stBottom"] > div {
        background: transparent !important;
    }
    div[data-testid="stChatInput"] {
        max-width: 380px !important;
        margin: 0 auto !important;
        padding: 0 8px 10px 8px !important;
    }
    div[data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 24px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06) !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.25) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #1f2937 !important;
        font-size: 13.5px !important;
        padding-left: 8px !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
    }
    button[data-testid="stChatInputSubmitButton"] {
        color: #7c3aed !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE INITIALIZATION ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! 👋 I'm Metro Buddy — your personal Surat Smart Metro guide!\n\nAsk me anything about routes, fares, stations, or timings. I'm also happy to just chat 😊\n\nWhat's on your mind?"
        }
    ]

# Count user messages to know if chat just started
user_msg_count = sum(1 for m in st.session_state.messages if m["role"] == "user")

# ---------- WIDGET CARD WRAPPER ----------
# Header Section & Welcome Banner
st.markdown("""
<div class="widget-container">
    <div class="widget-header">
        <div class="header-left">
            <span class="back-btn">&#x276E;</span>
            <div class="avatar-cluster">
                <span class="avatar-icon-1">🚇</span>
                <span class="avatar-icon-2">🤖</span>
            </div>
            <div class="header-info">
                <h4 class="header-title">Surat Metro</h4>
                <span class="header-subtitle">&#x23F1; Under 10 minutes</span>
            </div>
        </div>
        <div class="header-right">&#x2922;</div>
    </div>
    <div class="welcome-text">Welcome to Surat Metro Chat</div>
</div>
""", unsafe_allow_html=True)

# ---------- CHAT MESSAGES DISPLAY ----------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        escaped_user = html.escape(msg["content"]).replace("\n", "<br>")
        st.markdown(f"""
        <div class="user-row">
            <div class="user-bubble">{escaped_user}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        rendered_bot = md.render(msg["content"])
        st.markdown(f"""
        <div class="bot-row">
            <div class="bot-bubble">{rendered_bot}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- QUICK REPLY BUTTONS (Only when chat has just started) ----------
selected_prompt = None

if user_msg_count == 0:
    st.write("") # Tiny spacing
    if st.button("Route from Sarthana to DREAM City 🚇", key="qr_1"):
        selected_prompt = "What is the route from Sarthana to DREAM City?"
    if st.button("What is the fare structure? 🎫", key="qr_2"):
        selected_prompt = "What is the fare structure of Surat Metro?"
    if st.button("First & last train timings ⏱️", key="qr_3"):
        selected_prompt = "What are the first and last train timings and frequency?"

# ---------- CHAT INPUT & RESPONSE LOGIC ----------
user_input = st.chat_input("Type a message...")

if user_input:
    selected_prompt = user_input

if selected_prompt:
    # 1. Append user message
    st.session_state.messages.append({"role": "user", "content": selected_prompt})

    # 2. Get response from backend chatbot
    with st.spinner(""):
        bot_reply = get_response(selected_prompt)

    # 3. Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # 4. Immediate rerun to update UI
    st.rerun()