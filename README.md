# YouTube Video Downloader (CLI & Web UI) 🎥

A lightweight, robust Python application built with [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), [`ffmpeg`](https://ffmpeg.org/), and [`Gradio`](https://gradio.app/) to download high-quality YouTube videos directly in `.mp4` format.

Includes both a **Terminal CLI** interface and a modern **Web Interface**.

---

## ⚠️ Disclaimer & Caution

> **Use this tool at your own risk!**  
> This project is created strictly for **educational and personal archiving purposes only**. 
> - Downloading copyrighted material without permission may violate YouTube's [Terms of Service](https://www.youtube.com/t/terms) and local copyright laws.
> - The author of this repository assumes no liability or responsibility for any misuse or violation of third-party policies by users of this script.

---

## ✨ Features

- 🚀 **Highest Quality Video & Audio**: Automatically fetches the best video and audio streams (`bestvideo+bestaudio`).
- 🎬 **Native MP4 Output**: Merges streams seamlessly into a single `.mp4` container.
- 🌐 **Web Interface**: Interactive browser-based UI using Gradio.
- 🛡️ **Anti-Throttling Bypass**: Configured with mobile/web client fallback (`android`, `web`) to prevent `Connection reset by peer` errors.
- 🔄 **Auto-Retries**: Resilient against network drops with automatic fragment retries.

---

## 📋 Prerequisites

Make sure you have the following installed on your system:

1. **Python 3.8+**: [python.org](https://www.python.org/)
2. **FFmpeg**: Required for merging video and audio streams into MP4.
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
   - **Windows**: Install via `winget install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html).

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/youtube_video_downloader.git
   cd youtube_video_downloader
   ```

2. **Create and activate a virtual environment**:
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

## 🚀 How to Run

### Option 1: Terminal CLI
```bash
python3 main.py
```

### Option 2: Web Interface (Gradio)
```bash
python3 app.py
```
Then open `http://127.0.0.1:7860` in your browser!

---

## 🌐 Deploying to Hugging Face Spaces (Free Cloud Hosting)

1. Create a **New Space** on [Hugging Face](https://huggingface.co/new-space).
2. Select **Gradio** as the Space SDK.
3. Push/Upload all repository files (`app.py`, `requirements.txt`, `packages.txt`, `README.md`).
4. Hugging Face will automatically build and host your web application for free!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
