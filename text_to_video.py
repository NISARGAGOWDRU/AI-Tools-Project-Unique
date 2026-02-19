import os
import cv2
import numpy as np
from PIL import Image
from diffusers import DiffusionPipeline
from io import BytesIO
import streamlit as st
from concurrent.futures import ThreadPoolExecutor
import torch

# API Key
API_KEY = os.environ.get("HUGGING_FACE_API_KEY")
if not API_KEY:
    raise ValueError("Please set HUGGING_FACE_API_KEY environment variable")

# Log in to Hugging Face
from huggingface_hub import login
login(token=API_KEY)

# Initialize Diffusion Pipeline with GPU support
pipe = DiffusionPipeline.from_pretrained("ali-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16)
pipe.to("cuda")  # Use GPU

# Function to generate a single frame
def generate_frame(prompt):
    """
    Generate a single frame from the text prompt using the diffusion pipeline.

    Args:
        prompt (str): The text prompt for the image generation.

    Returns:
        bytes: The image in byte format.
    """
    result = pipe(prompt)
    image = result.images[0]
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# Generate a sequence of frames using threading
@st.cache
def text_to_image_sequence(prompt, num_frames=10):
    """
    Generate a sequence of images based on a text prompt.

    Args:
        prompt (str): The text prompt for generating the images.
        num_frames (int): The number of frames/images to generate.

    Returns:
        list: A list of generated image data (in byte format).
    """
    with ThreadPoolExecutor() as executor:
        frames = list(executor.map(lambda _: generate_frame(prompt), range(num_frames)))
    return frames

# Create a video directly from image data
def create_video_from_images(image_data, output_video_path, fps=1):
    """
    Create a video from a sequence of image data.

    Args:
        image_data (list): List of image data in byte format.
        output_video_path (str): Path to save the generated video.
        fps (int): Frames per second for the video.
    """
    # Initialize the video writer
    first_image = Image.open(BytesIO(image_data[0]))
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, first_image.size)

    for img_data in image_data:
        image = np.array(Image.open(BytesIO(img_data)))
        video_writer.write(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    video_writer.release()

# Streamlit frontend
def main():
    st.title("Optimized Text-to-Video Generator")
    st.markdown("Generate a video from your text prompts using optimized image generation and video stitching.")

    # Input text prompt
    prompt = st.text_input("Enter your text prompt:", "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k")

    num_frames = st.slider("Number of frames for the video", min_value=2, max_value=10, value=5)

    if st.button("Generate Video"):
        if prompt.strip():
            with st.spinner("Generating video..."):
                # Generate the sequence of images
                image_data = text_to_image_sequence(prompt, num_frames)

                # Create video from images
                output_video_path = "output_video.mp4"
                create_video_from_images(image_data, output_video_path, fps=1)

                # Display the generated video
                st.video(output_video_path)
        else:
            st.warning("Please enter a text prompt.")

if __name__ == "__main__":
    main()
