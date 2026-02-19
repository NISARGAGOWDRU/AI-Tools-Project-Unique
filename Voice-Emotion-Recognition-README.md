# 🎙️ Voice Emotion Recognition

A machine learning project that recognizes emotions from voice/audio signals using advanced audio feature extraction and classification algorithms.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![ML](https://img.shields.io/badge/ML-TensorFlow-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- 🎵 **Audio Feature Extraction** - Extracts MFCC, spectral features, and more
- 🤖 **Deep Learning Model** - Neural network for emotion classification
- 📊 **Real-time Analysis** - Process audio files and predict emotions
- 📈 **Multiple Emotions** - Detect Happy, Sad, Angry, Neutral, Fearful, etc.
- 📁 **Batch Processing** - Process multiple audio files at once

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **TensorFlow/Keras** - Deep learning framework
- **Librosa** - Audio analysis library
- **NumPy, Pandas** - Data processing
- **Scikit-learn** - Machine learning utilities
- **Matplotlib** - Data visualization

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/NISARGAGOWDRU/Voice-Emotion-Recognition.git
cd Voice-Emotion-Recognition

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Running the Project

```bash
# Run emotion recognition on audio file
python main.py --audio path/to/audio.wav

# Train model on dataset
python train.py --dataset path/to/dataset

# Evaluate model performance
python evaluate.py --model path/to/model.h5
```

---

## 📊 Usage Example

```python
from emotion_recognizer import EmotionRecognizer

# Initialize recognizer
recognizer = EmotionRecognizer(model_path='model.h5')

# Predict emotion from audio
emotion, confidence = recognizer.predict('audio.wav')
print(f"Emotion: {emotion}, Confidence: {confidence:.2%}")
```

---

## 📈 Model Performance

| Emotion | Precision | Recall | F1-Score |
|---------|-----------|--------|----------|
| Happy   | 0.92      | 0.89   | 0.90     |
| Sad     | 0.88      | 0.91   | 0.89     |
| Angry   | 0.94      | 0.92   | 0.93     |
| Neutral | 0.85      | 0.87   | 0.86     |

---

## 📁 Project Structure

```
Voice-Emotion-Recognition/
├── main.py                    # Main prediction script
├── train.py                   # Model training script
├── evaluate.py                # Model evaluation
├── models/
│   └── emotion_model.h5       # Trained model
├── data/
│   ├── train/                 # Training data
│   └── test/                  # Test data
├── utils/
│   ├── audio_processor.py     # Audio processing
│   └── feature_extractor.py   # Feature extraction
└── requirements.txt           # Dependencies
```

---

## 🎯 Supported Emotions

- 😊 **Happy**
- 😢 **Sad**
- 😠 **Angry**
- 😐 **Neutral**
- 😨 **Fearful**
- 🤢 **Disgusted**
- 😲 **Surprised**

---

## 📖 Documentation

For detailed documentation, see [DOCS.md](DOCS.md)

---

## 🤝 Contributing

Contributions welcome! Please fork and submit pull requests.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

**Made with ❤️ by NISARGA GOWDRU**
