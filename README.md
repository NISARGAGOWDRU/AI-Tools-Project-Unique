<<<<<<< HEAD
 # AI Tools Suite — Final Year Project

This repository bundles several Streamlit-based AI utilities built for a final-year project. The tools showcase integrations with large-model APIs and image-generation services to automate common content tasks.

Highlights
- Text-to-PowerPoint (`text_to_ppt.py`) — converts a topic and slide count into a downloadable PPTX using a generative model.
- Chatbot (`chatbot.py`) — simple Streamlit chatbot powered by the generative API.
- Blog generator, Email assistant, Quote generator, Resume creator, Social media post helper, Image→Text, Text→Image, Text→Audio, Text→Video — each implemented as a small Streamlit app in the project root.

Assets
- Visual assets (video/screenshots) are stored in `assets/` (copied from your machine). Example files you included:
  - `assets\clg ml proj.mp4`
  - `assets\Screenshot 2026-02-18 123345.png`
  - `assets\Screenshot 2026-02-18 123423.png`
  - `assets\Screenshot 2026-02-18 123412.png`
  - `assets\Screenshot 2026-02-18 123401.png`

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
