# YouTube Video Downloader (CLI) 🎥

A lightweight, robust Python command-line utility built with [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) and [`ffmpeg`](https://ffmpeg.org/) to download high-quality YouTube videos directly in `.mp4` format.

---

## ⚠️ Disclaimer & Caution

> **Use this tool at your own risk!**  
> This project is created strictly for **educational and personal archiving purposes only**. 
> - Downloading copyrighted material without permission may violate YouTube's [Terms of Service](https://www.youtube.com/t/terms) and local copyright laws.
> - The author of this repository assumes no liability or responsibility for any misuse or violation of third-party policies by users of this script.

---

## ✨ Features

- 🚀 **Highest Quality Video & Audio**: Automatically fetches the best video and audio streams (`bestvideo+bestaudio`).
- 🎬 **Native MP4 Output**: Merges streams seamlessly into a single `.mp4` container compatible with macOS (QuickTime), Windows, iOS, and Android.
- 🛡️ **Anti-Throttling Bypass**: Configured with mobile/web client fallback (`android`, `web`) to prevent connection resets.
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
   git clone https://github.com/charanteja-k/youtube_video_downloader.git
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

## 🚀 Usage

Run the script in your terminal:

```bash
python3 main.py
```

Paste the YouTube video URL when prompted:
```text
==================================================
🎬 YouTube Video Downloader (CLI)
==================================================

Enter YouTube URL: https://youtu.be/EXAMPLE_URL
```

The video will be downloaded into your project directory as a ready-to-watch `.mp4` file!

---

## 📄 License

Distributed under the MIT License.
