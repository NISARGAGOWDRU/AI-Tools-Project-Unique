import os
import requests
import streamlit as st
import base64
import google.generativeai as genai  # Ensure the genai library is installed
from google.generativeai import GenerativeModel

# Your API keys for Hugging Face and Google Gemini (from environment variables)
HUGGING_FACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")
GEMINI_API_KEY = os.environ.get("GENAI_API_KEY")

if not HUGGING_FACE_API_KEY or not GEMINI_API_KEY:
    raise ValueError("Please set HUGGING_FACE_API_KEY and GENAI_API_KEY environment variables")

# API endpoints
TEXT_TO_IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

# Authentication headers
hugging_face_headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

# Ensure that the API key is configured for the Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
DEFAULT_MODEL = os.environ.get('GENAI_MODEL', 'models/gemini-2.5-flash')

def generate_image_from_text(prompt):
    """
    Generate an image from a text prompt using Hugging Face's Stable Diffusion API.

    Args:
        prompt (str): The text prompt to generate the image.

    Returns:
        bytes: The generated image as a byte stream.
    """
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    # Send the POST request to generate the image
    response = requests.post(TEXT_TO_IMAGE_API_URL, headers=hugging_face_headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None


def generate_hashtags_from_prompt(prompt):
    """Generates hashtags based on the given prompt using Gemini."""
    try:
        # Initialize the model for content generation using configured default
        model = GenerativeModel(model_name=DEFAULT_MODEL)

        # Generate hashtags
        hashtags_prompt = f"Generate hashtags for the following content: '{prompt}'"
        response = model.generate_content(hashtags_prompt)

        hashtags = getattr(response, "text", None) or getattr(response, "content", None) or str(response)
        hashtags = hashtags.strip()

        # Return the generated hashtags as a string
        return hashtags
    except Exception as e:
        st.error(f"An error occurred while generating hashtags: {e}")
        return None

def download_link(content, filename="hashtags.txt"):
    """Generates a download link for the content."""
    b64_content = base64.b64encode(content.encode()).decode()  # Encode the content to base64
    download_url = f"data:file/txt;base64,{b64_content}"
    return download_url

def main():
    st.title("Social Media Post Generator")
    st.markdown("""Generate beautiful images and suggest hashtags for your social media posts using Hugging Face's Stable Diffusion and the Gemini API.""")

    # Input field for text prompt
    prompt = st.text_input("Enter your prompt:", "A futuristic cityscape with flying cars at sunset")

    if st.button("Generate Post"):
        if prompt.strip():
            with st.spinner("Generating image and hashtags..."):
                # Generate the image from the text prompt
                image_data = generate_image_from_text(prompt)
                if image_data:
                    st.image(image_data, caption="Generated Image", use_column_width=True)

                # Generate hashtags for the text prompt
                hashtags = generate_hashtags_from_prompt(prompt)
                if hashtags:
                    st.subheader("Suggested Hashtags")
                    st.write(hashtags)
                    # Optionally, provide a download link for the hashtags
                    download_url = download_link(hashtags)
                    st.markdown(f"[Download Hashtags]({download_url})")
        else:
            st.warning("Please enter a text prompt to generate the post.")

if __name__ == "__main__":
    main()
