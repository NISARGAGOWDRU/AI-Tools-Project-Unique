import os
import streamlit as st
import google.generativeai as genai

# Configure API key and default model via environment variables
genai.configure(api_key=os.environ.get('GENAI_API_KEY', 'AIzaSyBt3rmdSvRMU8lo3HnjJFELqzK1boA43m0'))
DEFAULT_MODEL = os.environ.get('GENAI_MODEL', 'models/gemini-2.5-flash')

# List of supported languages (including major Indian languages)
languages = [
    "English", "Spanish", "French", "German", "Italian", "Hindi",  
    "Chinese", "Japanese", "Russian", "Portuguese", "Arabic", 
    "Korean", "Dutch", "Turkish", "Swedish", "Polish", "Thai", 
    "Greek", "Czech", "Hungarian", "Romanian", "Bengali", "Telugu", 
    "Tamil", "Urdu", "Gujarati", "Malayalam", "Kannada", "Punjabi", 
    "Odia", "Maithili", "Assamese", "Sanskrit", "Marathi", "Rajasthani", 
    "Konkani", "Sindhi", "Dogri", "Kashmiri", "Nepali"
]

def translate_text(input_text, source_lang, target_lang):
    """Translate text using Gemini AI."""
    try:
        # Formulate the prompt for translation
        prompt = f"Translate the following text from {source_lang} to {target_lang}: {input_text}"

        # Use configured default model
        model = genai.GenerativeModel(model_name=DEFAULT_MODEL)
        response = model.generate_content(prompt)

        # Extract translated text from the response
        translated_text = response.text.strip()
        return translated_text
    except Exception as e:
        st.error(f"An error occurred while translating: {e}")
        return None

def main():
    """Main function to handle user input and translation."""
    st.title("Language Translation Bot")

    # Select source and target languages
    source_lang = st.selectbox("Select the source language", languages)
    target_lang = st.selectbox("Select the target language", languages)

    # Input field for text to translate
    input_text = st.text_area("Enter text to translate:")

    # Button to trigger translation
    translate_button = st.button("Translate")

    if translate_button and input_text:
        st.info("Translating... Please wait.")
        
        # Translate the input text
        translated_text = translate_text(input_text, source_lang, target_lang)

        if translated_text:
            # Display the translated text
            st.write(f"### Translated Text ({source_lang} to {target_lang}):")
            st.write(translated_text)

if __name__ == "__main__":
    main()
