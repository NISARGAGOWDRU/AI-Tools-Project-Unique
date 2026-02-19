#!/usr/bin/env python3
"""
Script to update GitHub repository descriptions using PyGithub
"""

import requests
import json

# Repository descriptions
repos = {
    "NISARGAGOWDRU/VOICE_EMOTION_RECOGNITION": "Machine learning project for emotion recognition from voice/audio signals. Uses audio feature extraction and classification algorithms.",
    "NISARGAGOWDRU/COMPUTERIZED-COGNITIVE-RETRAINING": "A web-based platform for computerized cognitive retraining and rehabilitation therapy. Built with HTML, CSS, and JavaScript.",
    "NISARGAGOWDRU/facerecognization-attendance-system": "Face recognition based attendance system using Python, OpenCV, and machine learning. Automates attendance tracking through facial recognition.",
    "NISARGAGOWDRU/mentoring-management-system": "A comprehensive mentoring management system built with PHP. Manages mentoring relationships, schedules, and progress tracking."
}

def update_repo_descriptions(token):
    """Update repository descriptions via GitHub API"""
    for repo, description in repos.items():
        url = f"https://api.github.com/repos/{repo}"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "description": description
        }
        
        try:
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"✓ Updated {repo}")
            else:
                print(f"✗ Failed to update {repo}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"✗ Error updating {repo}: {e}")

if __name__ == "__main__":
    print("To use this script, you need a GitHub Personal Access Token")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Create a new token with 'repo' scope")
    print("3. Set the GH_TOKEN environment variable or provide it when prompted")
    
    import os
    token = os.environ.get("GH_TOKEN")
    
    if not token:
        token = input("\nEnter your GitHub token: ").strip()
    
    if token:
        update_repo_descriptions(token)
    else:
        print("No token provided. Exiting.")
