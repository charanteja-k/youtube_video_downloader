import sys
import yt_dlp

print("=" * 50)
print("🎬 YouTube Video Downloader (CLI)")
print("=" * 50)

url = input("\nEnter YouTube URL: ").strip()

if not url:
    print("❌ Error: No URL provided.")
    sys.exit(1)

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s.%(ext)s',
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web']
        }
    },
    'nocheckcertificate': True,
    'retries': 10,
    'fragment_retries': 10,
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("\n✅ Download completed successfully!")
except KeyboardInterrupt:
    print("\n\n⚠️ Download cancelled by user.")
except Exception as e:
    print(f"\n❌ Error downloading video: {e}")