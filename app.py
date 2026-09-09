import os
import gradio as gr
import yt_dlp

try:
    import spaces
    has_spaces = True
except ImportError:
    has_spaces = False

def _download_logic(url):
    if not url or not url.strip():
        return None, "⚠️ Please enter a valid YouTube URL."

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'nocheckcertificate': True,
        'retries': 10,
        'fragment_retries': 10,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            output_file = f"{base}.mp4"
            return output_file, f"✅ Successfully downloaded: {info.get('title')}"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

if has_spaces:
    @spaces.GPU
    def download_youtube_video(url):
        return _download_logic(url)
else:
    def download_youtube_video(url):
        return _download_logic(url)

demo = gr.Interface(
    fn=download_youtube_video,
    inputs=gr.Textbox(
        label="YouTube URL",
        placeholder="Paste YouTube link here...",
        lines=1
    ),
    outputs=[
        gr.Video(label="Downloaded MP4 Video"),
        gr.Textbox(label="Status")
    ],
    title="🎬 YouTube Video Downloader Web App",
    description="Download high-resolution YouTube videos directly in MP4 format."
)

if __name__ == "__main__":
    demo.launch()
