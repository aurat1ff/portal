# utils.py

def fetch_gemini_response(prompt, chat_session):
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error fetching response: {e}"

def map_role(role):
    return {
        "user": "user",
        "model": "assistant",
        "system": "system"
    }.get(role, "assistant")
