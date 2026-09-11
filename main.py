import sys
import os
import shutil
import argparse
import yt_dlp

# Ensure stdout supports emojis on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def check_ffmpeg():
    """Verify that ffmpeg is installed and available on the system PATH."""
    if not shutil.which('ffmpeg'):
        print("❌ Error: 'ffmpeg' is not installed or not found in system PATH.")
        print("FFmpeg is required to merge video/audio streams and convert to MP3.")
        print("Please install it and try again.")
        sys.exit(1)


def get_interactive_inputs():
    """Prompt the user interactively for required inputs with validation."""
    print("=" * 50)
    print("🎬 YouTube Video Downloader (CLI)")
    print("=" * 50)

    url = ""
    while not url:
        url = input("\nEnter YouTube URL: ").strip()
        if not url:
            print("❌ Error: URL cannot be empty. Please try again.")

    print('\n Select Download Mode: ')
    print("  [1] Best Quality Video (1080p / 4K MP4)")
    print("  [2] Standard HD Video (720p MP4)")
    print("  [3] Audio Only (MP3)")

    choice = ""
    while choice not in ['1', '2', '3']:
        choice = input('\n Enter choice [1-3] only [default : 1]: ').strip() or '1'
        if choice not in ['1', '2', '3']:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

    is_playlist = 'list=' in url
    noplaylist = False

    if is_playlist:
        print('\n Playlist detected in url')
        print(' [ 1 ] Download only the single first video')
        print(' [ 2 ] Download the Entire playlist')
        
        pl_choice = ""
        while pl_choice not in ['1', '2']:
            pl_choice = input('Enter choice (1-2) [ default : 1 ] : ').strip() or '1'
            if pl_choice not in ['1', '2']:
                print("❌ Invalid choice. Please enter 1 or 2.")

        if pl_choice == '1':
            noplaylist = True

    return url, choice, noplaylist, is_playlist


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="🎬 YouTube Video Downloader (CLI)")
    parser.add_argument("url", nargs="?", help="The YouTube video or playlist URL")
    parser.add_argument("-m", "--mode", choices=['1', '2', '3'], 
                        help="Download mode: 1 (Best Quality), 2 (720p), 3 (Audio MP3)")
    parser.add_argument("-p", "--playlist-mode", choices=['1', '2'],
                        help="Playlist mode: 1 (Single video), 2 (Entire playlist)")
    parser.add_argument("-o", "--output", help="Custom output directory (default: ./downloads)")
    parser.add_argument("--insecure", action="store_true", help="Disable SSL certificate verification (not recommended)")
    
    return parser.parse_args()


def main():
    check_ffmpeg()
    args = parse_args()

    # Determine if we should use interactive mode or command line args
    if args.url:
        url = args.url
        choice = args.mode or '1'
        is_playlist = 'list=' in url
        
        if is_playlist:
            pl_choice = args.playlist_mode or '1'
            noplaylist = (pl_choice == '1')
        else:
            noplaylist = False
    else:
        url, choice, noplaylist, is_playlist = get_interactive_inputs()

    download_dir = args.output if args.output else os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'retries': 10,
        'fragment_retries': 10,
        'noplaylist': noplaylist,
        'writethumbnail': True,  # Download thumbnail for embedding
        'postprocessors': [],
    }

    if args.insecure:
        ydl_opts['nocheckcertificate'] = True

    # User option logic
    if choice == '3':
        # Audio only logic
        ydl_opts.update({
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        })
        ydl_opts['postprocessors'].extend([
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'EmbedThumbnail',  # Embed thumbnail as album art
            },
            {
                'key': 'FFmpegMetadata',  # Embed metadata tags
                'add_metadata': True,
            }
        ])

    elif choice == "2":
        # 720p Video logic
        ydl_opts.update({
            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        })
        ydl_opts['postprocessors'].extend([
            {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }
        ])

    else:
        # High quality video download logic (choice 1)
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        })
        ydl_opts['postprocessors'].extend([
            {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False,
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            }
        ])

    if is_playlist and not noplaylist:
        ydl_opts['outtmpl'] = os.path.join(download_dir, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s')

    # Setting download path
    print('\n Starting Download...')
    print(f" Output Directory: {download_dir}")
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