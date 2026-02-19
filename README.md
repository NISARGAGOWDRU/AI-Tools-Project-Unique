# AI Tools Suite — Final Year Project

This repository bundles several Streamlit-based AI utilities built for a final-year project. The tools showcase integrations with large-model APIs and image-generation services to automate common content tasks.

## Project Overview

A comprehensive suite of AI-powered applications designed to streamline content creation and automation. Each tool leverages cutting-edge generative AI and machine learning models to enhance productivity.

## Features & Tools

### 📊 Content Generation
- **Text-to-PowerPoint** (`text_to_ppt.py`) — Converts topics and specifications into fully formatted PPTX presentations using generative AI
- **Blog Generator** (`blog_creator.py`) — Creates engaging blog posts with SEO optimization
- **Email Generator** (`email_generator.py`) — Generates professional and personalized emails
- **Resume Creator** (`resume_creator.py`) — Builds optimized resumes from user input
- **Social Media Post Generator** (`social_media_post_generator.py`) — Creates platform-specific social media content

### 💬 Communication & Interaction
- **Chatbot** (`chatbot.py`) — Interactive Streamlit chatbot powered by generative AI APIs
- **Language Translation** (`Language_Translation.py`) — Multi-language translation capabilities

### 🎨 Media Processing
- **Image to Text** (`image_to_text.py`) — Extracts and analyzes text from images using OCR/vision models
- **Text to Image** (`text_to_image.py`) — Generates images from text descriptions
- **Text to Audio** (`text_to_audio.py`) — Converts text to natural-sounding audio
- **Text to Video** (`text_to_video.py`) — Creates videos from text prompts

### 🎯 Utilities
- **Quote Generator** (`quote_generator.py`) — Generates inspirational and contextual quotes
- **Frontend** (`frontend.py`) — Main UI dashboard for all tools
- **Language Translation** — Multi-language support

## Demo & Screenshots

### Project Demo Video
![Demo Video](assets/clg%20ml%20proj.mp4)

### Application Screenshots

**Screenshot 1: Main Interface**
![Screenshot 1](assets/Screenshot%202026-02-18%20123345.png)

**Screenshot 2: Feature Overview**
![Screenshot 2](assets/Screenshot%202026-02-18%20123423.png)

**Screenshot 3: Content Generation**
![Screenshot 3](assets/Screenshot%202026-02-18%20123412.png)

Quick start (development)
1. Create and activate a Python virtual environment and install requirements (example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set API keys as environment variables (do NOT hardcode keys):

```powershell
setx GENAI_API_KEY "your_gemini_api_key"
setx HUGGING_FACE_API_KEY "your_hf_api_key"
```

3. Run any app, for example:

```powershell
streamlit run "text_to_ppt.py"
```

Preparing and publishing to GitHub (recommended)
1. If you have the GitHub CLI (`gh`) installed and authenticated, run:

```powershell
gh repo create NISARGAGOWDRU/AI-Tools-Project-Unique --public --source=. --remote=origin --push
```

2. If you prefer manual steps (no `gh`):

```powershell
git init
git checkout -b main
git add .
git commit -m "Initial commit - AI Tools Suite"
git remote add origin https://github.com/NISARGAGOWDRU/AI-Tools-Project-Unique.git
git push -u origin main
```

Security notes
- Never commit API keys or credentials. Use `setx` / environment variables or a secrets manager.

Want me to push?
- I can either provide the exact commands you should run locally (safe), or push the repository for you if you provide a repository remote URL and a temporary personal access token. Tell me which you prefer.
=======
# AI-Tools-Project-Unique
A collection of Streamlit-based AI utilities built for a Final Year Project. The suite demonstrates integrations with generative APIs to automate content workflows: Text→PPT, chatbot, blog/email/resume generators, image captioning, text→image/audio/video, and social media helpers.
>>>>>>> 03ab1d0789358fdc2c80920216ba60c7a880c070
