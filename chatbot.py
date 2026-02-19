import os
import google.generativeai as genai
import streamlit as st

# Configure API key and default model via environment variables
genai.configure(api_key=os.environ.get("GENAI_API_KEY", "AIzaSyBt3rmdSvRMU8lo3HnjJFELqzK1boA43m0"))
DEFAULT_MODEL = os.environ.get("GENAI_MODEL", "models/gemini-2.5-flash")

# Initialize the model
model = genai.GenerativeModel(model_name=DEFAULT_MODEL)

# Function to get chatbot response
def chat_with_gpt(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit app setup
st.title("Chatbot with Google Gemini")
st.write("Type your message below and press 'Send'.")

user_input = st.text_input("You: ")
if st.button("Send"):
    if user_input:
        bot_response = chat_with_gpt(user_input)
        st.text_area("Bot:", value=bot_response, height=200)
