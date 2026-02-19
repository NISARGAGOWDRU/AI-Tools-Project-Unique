import os
import requests
import streamlit as st
import io
from PIL import Image

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HUGGINGFACE_API_KEY = os.environ.get("HUGGING_FACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("Please set HUGGING_FACE_API_KEY environment variable")

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def main():
    st.title("AI Text-to-Image Generator")
    st.write("Enter a prompt below to generate an image using AI.")

    prompt = st.text_input("Enter your prompt:", "A beautiful sunset over the mountains")

    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                image_bytes = query({"inputs": prompt})
                try:
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Generated Image")
                    
                    # Download button
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="Download Image",
                        data=buf.getvalue(),
                        file_name="generated_image.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.write("The API might be busy or the request failed. Please try again.")
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
