import os
import json
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_data
def load_config():
    with open("samething.json", encoding="utf8") as f:
        return json.load(f)

config = load_config()

INITIAL_BOT_MESSAGE = config.get(
    "initial_bot_message",
    "Hello, what do you need?"
)

@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="""
        You are GrammarBot.
        ONLY support:
        1. Phonetic symbols
        2. Synonyms
        """
    )

model = load_model()

def get_bot_response(user_input: str, language: str) -> str:
    user_input = user_input[:300]

    if language == "Vietnamese":
        prompt = f"""
        Chỉ hỗ trợ:
        1. Phiên âm
        2. Từ đồng nghĩa

        Nếu ngoài phạm vi, trả lời:
        "Tôi đang không hỗ trợ chức năng này."

        Yêu cầu:
        {user_input}
        """
    else:
        prompt = f"""
        ONLY support:
        1. Phonetic symbols
        2. Synonyms

        If outside scope, reply:
        "Sorry, I do not support this function."

        Request:
        {user_input}
        """

    response = model.generate_content(prompt)
    return response.text
