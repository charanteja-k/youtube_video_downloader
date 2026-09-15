import yt_dlp
import os

def download_subtitles(url, download_dir='downloads', lang='en'):
    """
    Downloads the subtitles of a YouTube video (manual or auto-generated) and saves them as a .srt file.
    """
    os.makedirs(download_dir, exist_ok=True)
    
    ydl_opts = {
        'skip_download': True, # We only want the subtitles, not the video
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'subtitlesformat': 'srt',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'nocheckcertificate': True,
        'retries': 10,
    }

    print(f"\n Fetching subtitles for {url}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Subtitles downloaded and saved in: {download_dir}")
    except Exception as e:
        print(f"\n❌ Error downloading subtitles: {e}")

if __name__ == "__main__":
    url = input("\nEnter YouTube URL for subtitles: ").strip()
    if url:
        download_subtitles(url)
    else:
        print("❌ Error: No URL provided.")