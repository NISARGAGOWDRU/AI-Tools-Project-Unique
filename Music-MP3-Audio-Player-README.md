# 🎵 Music MP3 Audio Player

A feature-rich Android music player application built with Java and Android Studio. Play, organize, and enjoy your favorite MP3 files with an intuitive interface.

![Java](https://img.shields.io/badge/Java-Latest-orange?style=flat-square)
![Android](https://img.shields.io/badge/Android-API%2021+-green?style=flat-square)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)

---

## ✨ Features

- 🎵 **MP3 Playback** - High-quality audio playback
- 📁 **File Management** - Browse and organize music files
- 🎚️ **Media Controls** - Play, pause, next, previous
- 📊 **Playlist Support** - Create and manage playlists
- 🔊 **Volume Control** - Adjustable volume levels
- ⏱️ **Progress Bar** - Track song progress
- 🎨 **Intuitive UI** - Clean and user-friendly design
- 🔀 **Shuffle & Repeat** - Multiple playback modes
- 🌙 **Dark Theme** - Easy on the eyes

---

## 🛠️ Technologies Used

- **Java** - Programming language
- **Android Studio** - Development IDE
- **Android SDK** - Mobile development framework
- **MediaPlayer API** - Audio playback
- **RecyclerView** - List management
- **SharedPreferences** - Data persistence
- **Android Material Design** - UI components

---

## 🚀 Quick Start

### Prerequisites

- Android Studio (Latest version)
- Android SDK 21+
- Java Development Kit (JDK 8+)
- Minimum 2GB RAM
- USB cable for testing

### Installation

```bash
# Clone repository
git clone https://github.com/NISARGAGOWDRU/Music-MP3-Audio-Player.git
cd Music-MP3-Audio-Player

# Open in Android Studio
# File → Open → Select project folder
```

### Building & Running

```
1. Open Android Studio
2. Select device/emulator
3. Click "Run" (Green play button)
4. App installs and launches
```

---

## 📖 User Guide

### Playing Music

1. **Open App** - Launch Music Player
2. **Browse Files** - Navigate to music folder
3. **Select Song** - Tap on any MP3 file
4. **Play Controls** - Use buttons to control playback
5. **Adjust Volume** - Use volume slider or device buttons

### Managing Playlists

1. **Create Playlist**
   - Tap "+" button
   - Enter playlist name
   - Add songs by dragging

2. **Edit Playlist**
   - Long press playlist
   - Select "Edit"
   - Add/remove songs

3. **Delete Playlist**
   - Long press playlist
   - Select "Delete"
   - Confirm action

---

## 📁 Project Structure

```
Music-MP3-Audio-Player/
├── src/main/
│   ├── java/com/example/musicplayer/
│   │   ├── MainActivity.java           # Main activity
│   │   ├── PlayerActivity.java         # Player screen
│   │   ├── PlaylistActivity.java       # Playlist management
│   │   ├── MusicService.java           # Background service
│   │   ├── adapters/
│   │   │   ├── SongAdapter.java        # Song list adapter
│   │   │   └── PlaylistAdapter.java    # Playlist adapter
│   │   └── models/
│   │       ├── Song.java               # Song model
│   │       └── Playlist.java           # Playlist model
│   ├── res/
│   │   ├── layout/
│   │   │   ├── activity_main.xml
│   │   │   └── activity_player.xml
│   │   ├── drawable/                  # Icons and images
│   │   ├── values/
│   │   │   ├── colors.xml
│   │   │   └── strings.xml
│   │   └── menu/                      # Menu resources
│   └── AndroidManifest.xml            # App manifest
├── build.gradle                       # Build configuration
└── README.md                          # Documentation
```

---

## 🎮 UI Components

### Main Screen
- List of songs from device
- Search functionality
- Sort options (Name, Date, Duration)
- Quick access buttons

### Player Screen
- Album art display
- Song title and artist
- Playback controls
- Progress bar with time
- Volume slider

### Playlist Screen
- Create new playlist
- View all playlists
- Edit/delete playlists
- Drag-drop songs

---

## ⚙️ Permissions Required

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.ACCESS_MEDIA_LOCATION" />
```

---

## 📊 Supported Formats

- ✅ MP3
- ✅ WAV
- ✅ AAC
- ✅ OGG
- ✅ FLAC

---

## 🎯 Features Detail

### Playback Modes
| Mode | Description |
|------|-------------|
| **Normal** | Play song once |
| **Repeat** | Repeat current song |
| **Repeat All** | Repeat entire playlist |
| **Shuffle** | Random song order |

---

## 🔄 Background Service

Music continues playing even when app is closed:

```java
// Service keeps audio playing
startService(new Intent(context, MusicService.class));
```

---

## 💾 Data Persistence

Playlists and preferences saved locally:

```java
// SharedPreferences
SharedPreferences prefs = getSharedPreferences("music_player", MODE_PRIVATE);
prefs.putString("current_playlist", playlistName);
```

---

## 🎨 Customization

Edit colors in `res/values/colors.xml`:

```xml
<color name="primary">#FF5722</color>
<color name="accent">#FFC107</color>
<color name="background">#121212</color>
```

---

## 🚨 Troubleshooting

### App Crashes on Launch
- Check permissions in settings
- Restart device
- Clear app cache

### No Songs Found
- Grant storage permissions
- Check file format
- Move MP3s to Music folder

### Audio Not Playing
- Check volume settings
- Verify audio format compatibility
- Restart app

---

## 🤝 Contributing

Contributions welcome! Improve:
- UI/UX design
- Audio quality options
- Equalizer features
- Lyrics display

---

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details

---

**Made with ❤️ by NISARGA GOWDRU**
