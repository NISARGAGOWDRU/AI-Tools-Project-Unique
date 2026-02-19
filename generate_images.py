#!/usr/bin/env python3
"""
Generate demo images for GitHub repositories
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create assets directory
os.makedirs('assets', exist_ok=True)

# Define image specifications
images_config = {
    'ai_tools_banner.png': {
        'size': (1200, 400),
        'bg_color': '#1a1a2e',
        'text': 'AI Tools Suite',
        'subtitle': 'Streamlit-based AI Utilities',
        'color': '#00d4ff'
    },
    'emotion_detection_chart.png': {
        'size': (800, 400),
        'bg_color': '#2c3e50',
        'text': 'Emotion Recognition',
        'subtitle': '95% Accuracy',
        'color': '#e74c3c'
    },
    'face_detection_demo.png': {
        'size': (800, 400),
        'bg_color': '#34495e',
        'text': 'Face Recognition System',
        'subtitle': '98% Detection Rate',
        'color': '#3498db'
    },
    'music_player_ui.png': {
        'size': (600, 400),
        'bg_color': '#1a1a1a',
        'text': 'Music Player',
        'subtitle': 'Android App',
        'color': '#e91e63'
    },
    'cognitive_games.png': {
        'size': (800, 400),
        'bg_color': '#2c3e50',
        'text': 'Cognitive Training',
        'subtitle': 'Brain Games Platform',
        'color': '#9b59b6'
    },
    'mentoring_dashboard.png': {
        'size': (1000, 500),
        'bg_color': '#1e3a5f',
        'text': 'Mentoring Dashboard',
        'subtitle': 'Relationship Management',
        'color': '#27ae60'
    }
}

def create_demo_image(filename, config):
    """Create a demo image with text"""
    
    img = Image.new('RGB', config['size'], config['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Try to use default font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 35)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    width, height = config['size']
    
    # Draw title
    title_text = config['text']
    subtitle_text = config['subtitle']
    title_color = config['color']
    
    # Calculate text position (center)
    draw.text((width // 2, height // 2 - 60), title_text, 
              font=title_font, fill=title_color, anchor='mm')
    draw.text((width // 2, height // 2 + 60), subtitle_text, 
              font=subtitle_font, fill='#ffffff', anchor='mm')
    
    # Save image
    img.save(filename)
    print(f'✓ Created {filename}')

# Generate all images
print("🎨 Creating demo images...")
print("-" * 50)

for filename, config in images_config.items():
    filepath = os.path.join('assets', filename)
    create_demo_image(filepath, config)

print("-" * 50)
print("✅ All demo images created successfully!")
