#!/usr/bin/env python3
"""
Generate SVG images for GitHub repositories
"""

import os
import base64

# Create assets directory
os.makedirs('assets', exist_ok=True)

# SVG images for each repository
svg_images = {
    'ai_tools_banner.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1200" height="300" fill="url(#grad1)"/>
  <text x="600" y="120" font-size="72" font-weight="bold" fill="#00d4ff" text-anchor="middle" font-family="Arial">
    🤖 AI Tools Suite
  </text>
  <text x="600" y="200" font-size="36" fill="#ffffff" text-anchor="middle" font-family="Arial">
    Streamlit-based AI Utilities | Final Year Project
  </text>
</svg>''',

    'emotion_detection.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" fill="#2c3e50"/>
  <text x="400" y="100" font-size="60" font-weight="bold" fill="#e74c3c" text-anchor="middle" font-family="Arial">
    🎙️ Voice Emotion Recognition
  </text>
  <text x="400" y="200" font-size="32" fill="#ecf0f1" text-anchor="middle" font-family="Arial">
    95% Accuracy • Real-time Processing
  </text>
  <text x="400" y="280" font-size="24" fill="#3498db" text-anchor="middle" font-family="Arial">
    Happy • Sad • Angry • Neutral • Fearful
  </text>
  <rect x="100" y="310" width="600" height="60" fill="#34495e" rx="5"/>
  <text x="400" y="345" font-size="20" fill="#ffffff" text-anchor="middle" font-family="Arial">
    TensorFlow • Librosa • Python
  </text>
</svg>''',

    'face_detection.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" fill="#34495e"/>
  <text x="400" y="100" font-size="60" font-weight="bold" fill="#3498db" text-anchor="middle" font-family="Arial">
    👤 Face Recognition System
  </text>
  <text x="400" y="200" font-size="32" fill="#ecf0f1" text-anchor="middle" font-family="Arial">
    98% Detection • Automated Attendance
  </text>
  <text x="400" y="280" font-size="24" fill="#2ecc71" text-anchor="middle" font-family="Arial">
    30 FPS Real-time Processing
  </text>
  <rect x="100" y="310" width="600" height="60" fill="#2c3e50" rx="5"/>
  <text x="400" y="345" font-size="20" fill="#ffffff" text-anchor="middle" font-family="Arial">
    OpenCV • Python • SQLite
  </text>
</svg>''',

    'music_player.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="400" fill="#1a1a1a"/>
  <circle cx="300" cy="150" r="80" fill="#e91e63"/>
  <text x="300" y="170" font-size="100" text-anchor="middle" font-family="Arial">
    🎵
  </text>
  <text x="300" y="280" font-size="48" font-weight="bold" fill="#e91e63" text-anchor="middle" font-family="Arial">
    Music Player
  </text>
  <text x="300" y="340" font-size="24" fill="#ffffff" text-anchor="middle" font-family="Arial">
    Android App • Java
  </text>
</svg>''',

    'cognitive_games.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="400" fill="#2c3e50"/>
  <text x="400" y="100" font-size="60" font-weight="bold" fill="#9b59b6" text-anchor="middle" font-family="Arial">
    🧠 Cognitive Retraining
  </text>
  <text x="400" y="200" font-size="32" fill="#ecf0f1" text-anchor="middle" font-family="Arial">
    Interactive Brain Games Platform
  </text>
  <text x="400" y="280" font-size="24" fill="#f39c12" text-anchor="middle" font-family="Arial">
    Memory • Attention • Problem-solving
  </text>
  <rect x="100" y="310" width="600" height="60" fill="#34495e" rx="5"/>
  <text x="400" y="345" font-size="20" fill="#ffffff" text-anchor="middle" font-family="Arial">
    HTML5 • CSS3 • JavaScript
  </text>
</svg>''',

    'mentoring_dashboard.svg': '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="1000" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect width="1000" height="500" fill="#1e3a5f"/>
  <text x="500" y="120" font-size="64" font-weight="bold" fill="#27ae60" text-anchor="middle" font-family="Arial">
    👨‍🎓 Mentoring Management System
  </text>
  <text x="500" y="220" font-size="32" fill="#ecf0f1" text-anchor="middle" font-family="Arial">
    Connect. Learn. Grow.
  </text>
  <g fill="#27ae60">
    <rect x="150" y="280" width="180" height="80" rx="5"/>
    <text x="240" y="330" font-size="18" fill="#ffffff" text-anchor="middle" font-family="Arial">Scheduling</text>
    
    <rect x="410" y="280" width="180" height="80" rx="5"/>
    <text x="500" y="330" font-size="18" fill="#ffffff" text-anchor="middle" font-family="Arial">Messaging</text>
    
    <rect x="670" y="280" width="180" height="80" rx="5"/>
    <text x="760" y="330" font-size="18" fill="#ffffff" text-anchor="middle" font-family="Arial">Analytics</text>
  </g>
  <rect x="100" y="410" width="800" height="60" fill="#2d5a7b" rx="5"/>
  <text x="500" y="445" font-size="20" fill="#ffffff" text-anchor="middle" font-family="Arial">
    PHP • MySQL • Bootstrap
  </text>
</svg>'''
}

# Save all SVG files
print("🎨 Creating demo images...")
print("-" * 50)

for filename, svg_content in svg_images.items():
    filepath = os.path.join('assets', filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f'✓ Created {filename}')

print("-" * 50)
print("✅ All demo images created successfully!")
