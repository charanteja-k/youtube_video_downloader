import yt_dlp

url = input("Enter URL : ")

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    'nocheckcertificate': True,
    'retries': 10,
    'fragment_retries': 10,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
