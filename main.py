import sys
import os
import yt_dlp
from sub import download_subtitles
from validurl import is_valid_youtube_url
from audio import get_multiple_audio_tracks, download_audio_tracks, get_full_lang_name, get_lang_code_from_name


def main():
    print("=" * 50)
    print("🎬 YouTube Video Downloader (CLI)")
    print("=" * 50)

    url = None
    while not url:
        user_input = input("\nEnter YouTube URL: ").strip()
        if not user_input:
            print("❌ Error: No URL provided.")
            continue
            
        if not is_valid_youtube_url(user_input):
            print("❌ Error: Invalid URL. Please enter a valid YouTube URL.")
            continue
            
        url = user_input
    
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

    sub_choice = input('\n Do you want to download subtitles too? (y/n) [default : n]: ').strip().lower()
    download_subs = sub_choice == 'y'

    print("\n Checking for multiple audio tracks...")
    audio_tracks = get_multiple_audio_tracks(url)
    selected_audio_tracks = {}
    
    if audio_tracks:
        available_langs = list(audio_tracks.keys())
        available_lang_names = [get_full_lang_name(l) for l in available_langs]
        print(f" Found multiple audio tracks in languages: {', '.join(available_lang_names)}")
        
        while True:
            lang_input = input(' Enter languages to download (comma separated, e.g. "telugu, hindi") or press Enter to skip: ').strip().lower()
            if not lang_input:
                break
                
            input_lang_names = [l.strip() for l in lang_input.split(',')]
            input_lang_codes = [get_lang_code_from_name(l) for l in input_lang_names]
            
            invalid_lang_names = []
            for i, code in enumerate(input_lang_codes):
                if code not in available_langs:
                    invalid_lang_names.append(input_lang_names[i])
            
            if invalid_lang_names:
                print(f" ❌ Invalid or misspelled languages: {', '.join(invalid_lang_names)}. Available languages are: {', '.join(available_lang_names)}")
            else:
                for code in input_lang_codes:
                    selected_audio_tracks[code] = audio_tracks[code]
                break
    else:
        print(" No additional audio tracks found.")

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
        if download_subs:
            download_subtitles(url, download_dir)
            print("\n Proceeding to download main video/audio...")
            
        if selected_audio_tracks:
            print("\n Downloading additional audio tracks...")
            download_audio_tracks(url, selected_audio_tracks, download_dir)
            print("\n Proceeding to download main video/audio...")
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n✅ Download completed! Files saved in: {download_dir}")
    except KeyboardInterrupt:
        print("\n\n⚠️ Download cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error downloading: {e}")
if __name__ == "__main__":
    main()