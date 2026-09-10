import sys
import os
import yt_dlp


def main():
    print("=" * 50)
    print("🎬 YouTube Video Downloader (CLI)")
    print("=" * 50)

    url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("❌ Error: No URL provided.")
        sys.exit(1)
    
    download_dir = os.path.join(os.getcwd(),'downloads')
    os.makedirs(download_dir, exist_ok=True)

    print('\n Select Download Mode: ')
    print("  [1] Best Quality Video (1080p / 4K MP4)")
    print("  [2] Standard HD Video (720p MP4)")
    print("  [3] Audio Only (MP3)")

    choice = input('\n Enter choice [1-3] only [default : 1]').strip() or '1'

    # Handling playlist url detection

    is_playlist = 'list=' in url
    noplaylist = False

    if is_playlist:
        print('\n Playlist detected in url')
        print(' [ 1 ] Download only the single first video')
        print(' [ 2 ] Download the Entire playlist')
        pl_choice = input('Enter choice (1-2) [ default : 1 ] : ').strip() or '1'

        if pl_choice == '1':
            noplaylist = True

    ydl_opts = {
        'nocheckcertificate': True,
        'retries': 10,
        'fragment_retries': 10,
        'noplaylist': noplaylist,
    }

    #User option logic

    #only audio logic
    if choice == '3' : 
        ydl_opts.update({
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
    })

    #low quality mp4 download logic
    elif choice == "2":
        # 720p Video
        ydl_opts.update({
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        })

        
    #high quality video download logic
    else:
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        })


    if is_playlist and not noplaylist :
        ydl_opts['outtmpl'] = os.path.join(download_dir, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s')

    #setting download path
    print('\n Starting Download')
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Download completed! Files saved in: {download_dir}")
    except KeyboardInterrupt:
        print("\n\n⚠️ Download cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error downloading: {e}")
if __name__ == "__main__":
    main()