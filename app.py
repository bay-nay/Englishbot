# app.py
import streamlit as st
import uuid
from logic import get_bot_response, INITIAL_BOT_MESSAGE

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="English GrammarBot",
    page_icon="📘",
    layout="centered"
)

# ================== INIT SESSION ==================
if "conversations" not in st.session_state:
    conv_id = str(uuid.uuid4())
    st.session_state.conversations = {
        conv_id: {
            "title": "New conversation",
            "messages": [
                {"role": "assistant", "content": INITIAL_BOT_MESSAGE}
            ]
        }
    }
    st.session_state.current_conv_id = conv_id

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    language = st.selectbox(
        "🌍 Language",
        ["English", "Vietnamese"]
    )

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    st.divider()

    # ===== New conversation =====
    if st.button("🆕 New conversation", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.conversations[new_id] = {
            "title": "New conversation",
            "messages": [
                {"role": "assistant", "content": INITIAL_BOT_MESSAGE}
            ]
        }
        st.session_state.current_conv_id = new_id
        st.rerun()

    # ===== Conversation history (CLICKABLE) =====
    st.markdown("## 💬 Conversation History")

    for conv_id, conv in st.session_state.conversations.items():
        is_active = conv_id == st.session_state.current_conv_id

        if st.button(
            f"📘 {conv['title']}",
            key=conv_id,
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_conv_id = conv_id
            st.rerun()

# ================== MAIN TITLE ==================
st.markdown(
    """
    <h1 style='text-align:center;'>📘 English GrammarBot</h1>
    <p style='text-align:center; color:gray;'>
        Find phonetic and synonym
    </p>
    """,
    unsafe_allow_html=True
)

def english_chatbot():

    current_conv = st.session_state.conversations[
        st.session_state.current_conv_id
    ]

    # ===== CHAT HISTORY =====
    for msg in current_conv["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ===== USER INPUT =====
    prompt = st.chat_input("✍️ Enter the word you want to look up")
    if prompt:
        # User message
        current_conv["messages"].append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("🤖 English Bot is thinking..."):
            bot_reply = get_bot_response(prompt, language)

        # Bot message
        current_conv["messages"].append(
            {"role": "assistant", "content": bot_reply}
        )

        # Đặt title theo câu đầu tiên
        if current_conv["title"] == "New conversation":
            current_conv["title"] = f"Tra từ: {prompt[:20]}"

        with st.chat_message("assistant"):
            st.write(bot_reply)

# ================== RUN ==================
if __name__ == "__main__":
    english_chatbot()
