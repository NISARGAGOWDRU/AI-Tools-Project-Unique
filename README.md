# 🤖 AI Tools Suite — Final Year Project

A comprehensive collection of **Streamlit-based AI utilities** that automate content creation and processing. This suite integrates cutting-edge generative AI and machine learning models to enhance productivity across multiple domains.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🎥 Demo & Screenshots

### 📹 Project Demo Video
Watch the application in action:
```
assets/clg ml proj.mp4
```

### 📸 Application Screenshots

| Main Dashboard | Features Overview | Content Generation |
|---|---|---|
| ![Dashboard](assets/Screenshot%202026-02-18%20123345.png) | ![Features](assets/Screenshot%202026-02-18%20123423.png) | ![Generation](assets/Screenshot%202026-02-18%20123412.png) |

---

## ✨ Features & Tools

### 📝 Content Generation Tools
| Tool | Description | Technology |
|------|-------------|-----------|
| **Text-to-PowerPoint** | Converts topics into fully formatted PPTX presentations | Python, PPTX, Gemini AI |
| **Blog Generator** | Creates engaging, SEO-optimized blog posts | Python, NLP, Gemini API |
| **Email Generator** | Generates professional and personalized emails | Python, Template Engine |
| **Resume Creator** | Builds optimized, ATS-friendly resumes | Python, DOCX, Templates |
| **Social Media Generator** | Creates platform-specific social posts | Python, Content AI |
| **Quote Generator** | Generates inspirational and contextual quotes | Python, AI Models |

### 💬 Communication Tools
| Tool | Description | Technology |
|------|-------------|-----------|
| **AI Chatbot** | Interactive conversation with AI | Python, Streamlit, Gemini API |
| **Language Translator** | Multi-language translation | Python, HuggingFace Transformers |

### 🎨 Media Processing Tools
| Tool | Description | Technology |
|------|-------------|-----------|
| **Image to Text** | Extracts text from images (OCR) | Python, OpenCV, Vision AI |
| **Text to Image** | Generates images from descriptions | Python, Stable Diffusion/DALL-E |
| **Text to Audio** | Converts text to speech | Python, Text-to-Speech APIs |
| **Text to Video** | Creates videos from prompts | Python, Video Generation APIs |

### 🎯 Main Interface
- **Frontend Dashboard** — Unified UI for all tools

---

## 🛠️ Technologies & Stack

```
Backend:
├── Python 3.8+
├── Streamlit (Web Framework)
├── Google Gemini API (Generative AI)
├── HuggingFace Transformers (ML Models)
├── OpenCV (Image Processing)
├── Librosa (Audio Processing)
└── PPTX (PowerPoint Generation)

APIs:
├── Google Gemini API
├── HuggingFace API
├── Text-to-Speech APIs
├── Image Generation APIs
└── Video Generation APIs

Database:
└── File-based Storage (SQLite optional)
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+**
- **pip** package manager
- **Git**
- **API Keys:** Gemini, HuggingFace

### Step 1: Clone Repository
```bash
git clone https://github.com/NISARGAGOWDRU/AI-Tools-Project-Unique.git
cd AI-Tools-Project-Unique
```

### Step 2: Create Virtual Environment
```powershell
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
```powershell
# Windows (PowerShell)
setx GENAI_API_KEY "your_gemini_api_key"
setx HUGGING_FACE_API_KEY "your_hf_api_key"

# Linux/Mac (Bash)
export GENAI_API_KEY="your_gemini_api_key"
export HUGGING_FACE_API_KEY="your_hf_api_key"
```

### Step 5: Run Application
```bash
# Launch main dashboard
streamlit run frontend.py

# Or run individual tools
streamlit run text_to_ppt.py
streamlit run chatbot.py
streamlit run blog_creator.py
streamlit run image_to_text.py
```

---

## 📋 Tool Usage Examples

### 1️⃣ Text to PowerPoint
```
Input:  Topic: "Machine Learning Basics"
        Slides: 10
Output: presentation.pptx (downloaded)
```

### 2️⃣ Blog Generator
```
Input:  Topic: "AI in Healthcare"
        Keyword: "Medical AI"
Output: Full blog post with SEO optimization
```

### 3️⃣ Chatbot
```
Input:  User: "Explain quantum computing"
Output: AI-powered response with details
```

### 4️⃣ Email Generator
```
Input:  Type: "Job Application"
        Details: Company, Position
Output: Professional email template
```

### 5️⃣ Image to Text
```
Input:  Image file (JPG, PNG)
Output: Extracted text + Analysis
```

### 6️⃣ Text to Image
```
Input:  Prompt: "Beautiful sunset over mountains"
Output: Generated image (PNG)
```

### 7️⃣ Text to Audio
```
Input:  Text: "Hello, welcome to AI Tools"
Output: Audio file (MP3/WAV)
```

### 8️⃣ Resume Creator
```
Input:  Name, Experience, Skills
Output: Formatted resume (DOCX/PDF)
```

---

## 📁 Project Structure

```
AI-Tools-Project-Unique/
│
├── 🖥️ Frontend & Main
│   ├── frontend.py                    # Main dashboard
│   └── __pycache__/
│
├── 📝 Content Generation
│   ├── text_to_ppt.py                 # PowerPoint generator
│   ├── blog_creator.py                # Blog creator
│   ├── email_generator.py             # Email generator
│   ├── resume_creator.py              # Resume builder
│   ├── social_media_post_generator.py # Social media posts
│   └── quote_generator.py             # Quote generator
│
├── 💬 Communication
│   ├── chatbot.py                     # AI chatbot
│   └── Language_Translation.py         # Translator
│
├── 🎨 Media Processing
│   ├── image_to_text.py               # OCR
│   ├── text_to_image.py               # Image generation
│   ├── text_to_audio.py               # Audio generation
│   └── text_to_video.py               # Video generation
│
├── 📦 Assets & Config
│   ├── assets/                        # Demo media
│   │   ├── clg ml proj.mp4           # Demo video
│   │   ├── Screenshot 2026-02-18 123345.png
│   │   ├── Screenshot 2026-02-18 123423.png
│   │   └── Screenshot 2026-02-18 123412.png
│   │
│   ├── requirements.txt               # Dependencies
│   ├── .gitignore                     # Git ignore rules
│   ├── LICENSE                        # MIT License
│   └── README.md                      # Documentation
│
└── 🔧 Development
    └── prepare_repo.ps1               # Setup script
```

---

## 🔐 Security Best Practices

⚠️ **Critical:** Never hardcode API keys!

### ✅ Do's
```python
# ✓ Use environment variables
import os
api_key = os.getenv('GENAI_API_KEY')
hf_token = os.getenv('HUGGING_FACE_API_KEY')
```

### ❌ Don'ts
```python
# ✗ Never do this!
api_key = "ghp_xxxxxxxxxxxx"  # WRONG!
```

### .gitignore Rules
```
# Environment & Secrets
.env
.env.local
api_keys.txt

# Virtual Environment
.venv/
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

---

## 📦 Installation & Dependencies

### Key Requirements
- **streamlit** - Web application framework
- **google-generativeai** - Gemini API
- **transformers** - HuggingFace models
- **opencv-python** - Image processing
- **librosa** - Audio processing
- **python-pptx** - PowerPoint generation
- **requests** - HTTP client

### Install All
```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/YourFeature`
3. **Commit** changes: `git commit -m 'Add YourFeature'`
4. **Push** branch: `git push origin feature/YourFeature`
5. **Open** Pull Request

### Contribution Guidelines
- Follow Python PEP 8 style guide
- Add comments for complex logic
- Test your changes before submitting
- Update README if adding new features

---

## 🐛 Troubleshooting

### Issue: "Module not found" Error
```bash
# Solution: Install requirements
pip install -r requirements.txt
```

### Issue: API Key Not Working
```bash
# Check environment variable is set
echo $GENAI_API_KEY  # Linux/Mac
echo %GENAI_API_KEY%  # Windows
```

### Issue: Streamlit Port Already in Use
```bash
# Use different port
streamlit run frontend.py --server.port 8502
```

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for full details.

```
MIT License

Copyright (c) 2026 NISARGA GOWDRU

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

---

## 👤 Author & Contact

**NISARGA GOWDRU**
- 🔗 GitHub: [@NISARGAGOWDRU](https://github.com/NISARGAGOWDRU)
- 📧 Email: nisargagowdru@email.com
- 🌐 Portfolio: [Your Website]

---

## 💬 Support & Help

### Getting Help
1. 📖 Check [Issues](https://github.com/NISARGAGOWDRU/AI-Tools-Project-Unique/issues)
2. 🔍 Search existing discussions
3. 📝 Create new issue with:
   - Detailed description
   - Error message/screenshot
   - Steps to reproduce
   - Your environment info

### Community
- 💡 Share ideas and suggestions
- 🐛 Report bugs
- 🚀 Request features
- 📚 Share use cases

---

## 🙏 Acknowledgments

**Special Thanks To:**
- 🤖 **Google** for Gemini API
- ⚡ **Streamlit** for amazing framework
- 🤖 **HuggingFace** for ML models
- 👥 **Contributors** for support
- ⭐ **Users** for feedback

---

## 📊 Project Stats

- **Languages:** Python, HTML, CSS, JavaScript
- **Tools:** 12+ AI-powered applications
- **APIs:** 5+ integration services
- **Lines of Code:** 5000+
- **Last Updated:** February 2026

---

## 🎯 Roadmap

### Planned Features
- [ ] Mobile app (React Native)
- [ ] Enhanced batch processing
- [ ] Database integration (PostgreSQL)
- [ ] Advanced analytics dashboard
- [ ] Multi-language UI support
- [ ] Docker containerization
- [ ] API REST endpoints
- [ ] Real-time collaboration features

---

## ⭐ Show Your Support

If this project helped you, please:
- ⭐ **Star** this repository
- 🔀 **Fork** and contribute
- 📢 **Share** with others
- 💬 **Provide feedback**

---

**Made with ❤️ by NISARGA GOWDRU**

**Last Updated:** February 19, 2026
