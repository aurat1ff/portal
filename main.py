import streamlit as st
import os
import google.generativeai as genai
from utils import fetch_gemini_response, map_role

# --------------------------
# Streamlit App Config
# --------------------------
st.set_page_config(
    page_title="Aura Unchained!",
    page_icon="🤖",
    layout="wide",
)

# --------------------------
# API Configuration
# --------------------------
# Local dev or Streamlit secrets
api_key = os.getenv("GEMINI_API_KEY", st.secrets.get("gemini", {}).get("api_key"))
genai.configure(api_key=api_key)

# --------------------------
# Session State: Chat
# --------------------------
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Or 1.5-pro / 2.5-pro
        generation_config={"temperature": 0.7},
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --------------------------
# Page UI
# --------------------------
st.title("🪐 Set your inner Aura free!")

# Render chat history
for msg in st.session_state.chat_session.history:
    with st.chat_message(map_role(msg["role"])):
        st.markdown(msg["content"])

# User prompt
user_input = st.chat_input("Ask Aura...")
if user_input:
    st.chat_message("user").markdown(user_input)

    # Get response from Gemini
    gemini_response = fetch_gemini_response(user_input, st.session_state.chat_session)

    # Display response
    with st.chat_message("assistant"):
        st.markdown(gemini_response)

    # Save messages to session
    st.session_state.chat_session.history.extend([
        {"role": "user", "content": user_input},
        {"role": "model", "content": gemini_response}
    ])
