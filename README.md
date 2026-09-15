# 🎬 Ultimate YouTube Video & Audio Downloader (CLI)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red.svg)](https://github.com/yt-dlp/yt-dlp)

A powerful, interactive command-line application built in Python using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and [`ffmpeg`](https://ffmpeg.org/). Easily download YouTube videos in maximum quality (1080p/4K MP4), extract high-quality MP3 audio, and manage playlist downloads with a clean terminal interface.

---

## ⚠️ Disclaimer & Caution

> **Use this tool at your own risk!**  
> This project is created strictly for **educational and personal archiving purposes only**. 
> - Downloading copyrighted material without permission may violate YouTube's [Terms of Service](https://www.youtube.com/t/terms) and local copyright laws.
> - The author of this repository assumes no liability or responsibility for any misuse or violation of third-party policies by users of this script.

---

## ✨ Features

- 🌐 **URL Validation**: Automatically verifies and ensures that only valid YouTube links are processed.
- 🎥 **Multiple Video Quality Options**: Download in **Ultra HD / 1080p / 4K** or **720p HD** (for smaller file size).
- 🎵 **Audio Extraction (MP3)**: Convert YouTube videos directly to **192kbps MP3** audio (perfect for songs, podcasts, and lectures).
- 🔊 **Multiple Audio Tracks**: Automatically detects dubbed videos with multiple audio languages, lists them using their full language names, and lets you select specific tracks to download.
- 📝 **Subtitle Downloads**: Provides an interactive prompt to effortlessly download video subtitles (.vtt files).
- 🛑 **Smart Playlist Handling**: Detects playlist URLs and lets you choose between downloading **only the single video** or the **entire playlist**.
- 📂 **Auto-Organized Downloads**: Automatically saves all media inside a dedicated `downloads/` directory (playlists get their own subfolders!).
- 🎬 **Native MP4 Merging**: Uses `ffmpeg` to remux separate video and audio streams into standard, widely-compatible `.mp4` containers.
- 🛡️ **Network Resilient**: Automatic retries for fragmented media streams and SSL bypass settings.

---

## 📋 Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.8+**: Download from [python.org](https://www.python.org/)
2. **FFmpeg**: Required for merging video/audio streams and converting to MP3.
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
   - **Windows**: Install via `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html).

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/charanteja-k/youtube_video_downloader.git
   cd youtube_video_downloader
   ```

2. **Create and activate a virtual environment** *(recommended)*:
   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage Guide

Run the script from your terminal:

```bash
python3 main.py
```

### Terminal Walkthrough Example:

```text
==================================================
🎬 YouTube Video Downloader (CLI)
==================================================

Enter YouTube URL: https://www.youtube.com/watch?v=EXAMPLE_VIDEO

 Select Download Mode: 
  [1] Best Quality Video (1080p / 4K MP4)
  [2] Standard HD Video (720p MP4)
  [3] Audio Only (MP3)

 Enter choice [1-3] only [default : 1]: 1

 Starting Download...
[info] Downloading 1 format(s): 616+251
[Merger] Merging formats into "downloads/Video_Title.mp4"

✅ Download completed! Files saved in: /path/to/youtube_video_downloader/downloads
```

---

## 📁 Project Structure

```text
youtube_video_downloader/
├── main.py              # Main interactive CLI script
├── requirements.txt     # Python dependencies (yt-dlp)
├── .gitignore           # Git ignore file (excludes venv and downloads/)
└── README.md            # Project documentation
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
