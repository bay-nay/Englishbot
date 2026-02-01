# chatbot_logic.py
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load môi trường
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Load config
with open('samething.json', 'r', encoding="utf8") as f:
    config = json.load(f)

INITIAL_BOT_MESSAGE = config.get(
    'initial_bot_message',
    'Hello,what do you need'
)

# Khởi tạo model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="""
    Bạn tên là Grammarbot, một trợ lý AI có nhiệm vụ hỗ trợ giải đáp thông tin về những từ tiếng anh.
    Các chức năng mà bạn hỗ trợ gồm:
    1. Dựa vào từ người dùng nhập vào và tìm phonetic symbol
    2. Tìm synonym của từ được tìm.
    Ngoài hai chức năng trên, bạn không hỗ trợ chức năng nào khác.
    Đối với các câu hỏi ngoài chức năng mà bạn hỗ trợ, trả lời bằng:
    'Tôi đang không hỗ trợ chức năng này.'
    Hãy nói chuyện lịch sự.Nói tiếng anh hoặc tiếng việt dựa theo phần language
    """
)

def get_bot_response(user_input: str) -> str:
    """Gửi câu hỏi tới Gemini và trả về câu trả lời"""
    response = model.generate_content(user_input)
    return response.text

def get_bot_response(user_input: str, language: str) -> str:

    if language == "Vietnamese":
        prompt = f"""
        Bạn là GrammarBot.

        CHỈ hỗ trợ:
        1. Phiên âm (phonetic symbol)
        2. Từ đồng nghĩa (synonym)

        Nếu câu hỏi KHÔNG liên quan đến 2 chức năng trên,
        hãy trả lời đúng một câu:
        "Tôi đang không hỗ trợ chức năng này."

        Trả lời bằng tiếng Việt.

        Yêu cầu người dùng:
        {user_input}
        """
    else:
        prompt = f"""
        You are GrammarBot.

        ONLY support:
        1. Phonetic symbols
        2. Synonyms

        If the request is OUTSIDE these functions,
        reply with exactly:
        "Sorry, I do not support this function."

        Answer in English.

        User request:
        {user_input}
        """

    response = model.generate_content(prompt)
    return response.text

