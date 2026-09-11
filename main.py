import sys
import os
import shutil
import argparse
import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

# Ensure stdout supports emojis on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

console = Console()

def check_ffmpeg():
    """Verify that ffmpeg is installed and available on the system PATH."""
    if not shutil.which('ffmpeg'):
        console.print("[bold red]❌ Error:[/bold red] 'ffmpeg' is not installed or not found in system PATH.")
        console.print("FFmpeg is required to merge video/audio streams and convert to MP3.")
        console.print("Please install it and try again.")
        sys.exit(1)

def get_interactive_inputs():
    """Prompt the user interactively for required inputs with rich UI."""
    console.print(Panel.fit("[bold cyan]🎬 YouTube Video Downloader (CLI)[/bold cyan]", border_style="cyan"))

    url = ""
    while not url:
        url = Prompt.ask("\n[bold yellow]Enter YouTube URL[/bold yellow]").strip()
        if not url:
            console.print("[red]❌ Error: URL cannot be empty. Please try again.[/red]")

    console.print("\n[bold cyan]Select Download Mode:[/bold cyan]")
    console.print("  [1] Best Quality Video (1080p / 4K MP4)")
    console.print("  [2] Standard HD Video (720p MP4)")
    console.print("  [3] Audio Only (MP3)")

    choice = Prompt.ask("\n[bold yellow]Enter choice[/bold yellow]", choices=['1', '2', '3'], default='1')

    is_playlist = 'list=' in url
    noplaylist = False

    if is_playlist:
        console.print("\n[bold magenta]Playlist detected in URL[/bold magenta]")
        console.print("  [1] Download only the single first video")
        console.print("  [2] Download the Entire playlist")
        
        pl_choice = Prompt.ask("[bold yellow]Enter choice[/bold yellow]", choices=['1', '2'], default='1')
        if pl_choice == '1':
            noplaylist = True

    download_subtitles = False
    if choice in ['1', '2']: # Subtitles make sense for video
        download_subtitles = Confirm.ask("\n[bold yellow]Do you want to download English subtitles (.srt)?[/bold yellow]", default=False)

    return url, choice, noplaylist, is_playlist, download_subtitles

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="🎬 YouTube Video Downloader (CLI)")
    parser.add_argument("url", nargs="?", help="The YouTube video or playlist URL")
    parser.add_argument("-m", "--mode", choices=['1', '2', '3'], 
                        help="Download mode: 1 (Best Quality), 2 (720p), 3 (Audio MP3)")
    parser.add_argument("-p", "--playlist-mode", choices=['1', '2'],
                        help="Playlist mode: 1 (Single video), 2 (Entire playlist)")
    parser.add_argument("-s", "--subtitles", action="store_true", help="Download English subtitles (.srt)")
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
        download_subtitles = args.subtitles
    else:
        url, choice, noplaylist, is_playlist, download_subtitles = get_interactive_inputs()

    download_dir = args.output if args.output else os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'retries': 10,
        'fragment_retries': 10,
        'noplaylist': noplaylist,
        'writethumbnail': True,  # Download thumbnail for embedding
        'postprocessors': [],
        'quiet': True,
        'no_warnings': True,
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

    if download_subtitles and choice in ['1', '2']:
        ydl_opts.update({
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'srt/best',
        })
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        })
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegEmbedSubtitle',
        })

    if is_playlist and not noplaylist:
        ydl_opts['outtmpl'] = os.path.join(download_dir, '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s')

    console.print(f"\n[bold green]Starting Download...[/bold green]")
    console.print(f"[cyan]Output Directory:[/cyan] {download_dir}")

    # Set up rich progress bar hook
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        
        task_id = progress.add_task("[cyan]Downloading...", total=None)

        def yt_dlp_hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    progress.update(task_id, total=total, completed=downloaded)
            elif d['status'] == 'finished':
                progress.update(task_id, description="[green]Processing/Merging...[/green]")

        ydl_opts['progress_hooks'] = [yt_dlp_hook]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            console.print(Panel.fit(f"[bold green]✅ Download completed![/bold green]\nFiles saved in: {download_dir}", border_style="green"))
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]⚠️ Download cancelled by user.[/bold yellow]")
        except Exception as e:
            console.print(f"\n[bold red]❌ Error downloading:[/bold red] {e}")

if __name__ == "__main__":
    main()