import yt_dlp   


print('=+'*50,end='')
print('\nYoutube Video Downloader')
print('=+'*50,end='')

url = input("\nEnter URL : ")

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
    