import yt_dlp
import os

LANG_MAP = {
    'ar': 'Arabic', 'bn': 'Bengali', 'de': 'German', 'es': 'Spanish', 'fr': 'French',
    'hi': 'Hindi', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean',
    'ml': 'Malayalam', 'pl': 'Polish', 'pt': 'Portuguese', 'ru': 'Russian', 'ta': 'Tamil',
    'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish', 'vi': 'Vietnamese',
    'zh-Hans': 'Chinese (Simplified)', 'zh-Hant': 'Chinese (Traditional)', 'en': 'English',
    'nl': 'Dutch', 'pa': 'Punjabi', 'ur': 'Urdu', 'fa': 'Persian', 'mr': 'Marathi',
    'gu': 'Gujarati', 'kn': 'Kannada', 'or': 'Odia', 'sv': 'Swedish', 'fi': 'Finnish',
    'no': 'Norwegian', 'da': 'Danish', 'el': 'Greek', 'he': 'Hebrew', 'cs': 'Czech',
    'hu': 'Hungarian', 'ro': 'Romanian', 'uk': 'Ukrainian', 'ms': 'Malay', 'tl': 'Tagalog'
}

def get_full_lang_name(code):
    return LANG_MAP.get(code, code)

def get_lang_code_from_name(name):
    name = name.lower()
    for code, full_name in LANG_MAP.items():
        if full_name.lower() == name:
            return code
    return name

def get_multiple_audio_tracks(url):
    """
    Checks for multiple audio tracks and returns a dictionary of language -> format_id.
    Returns an empty dict if no other audio tracks are available (1 or fewer languages).
    """
    ydl_opts_info = {'quiet': True, 'nocheckcertificate': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception:
        return {}

    formats = info.get('formats', [])
    
    # Filter for audio-only formats
    audio_formats = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
    
    best_audio_by_lang = {}
    
    for f in audio_formats:
        lang = f.get('language')
        # We only consider tracks that have a defined language
        if lang:
            abr = f.get('abr') or 0
            best_abr = best_audio_by_lang[lang].get('abr') if lang in best_audio_by_lang else 0
            best_abr = best_abr or 0
            
            if lang not in best_audio_by_lang or abr > best_abr:
                best_audio_by_lang[lang] = f

    # If there are multiple unique languages, we return them
    if len(best_audio_by_lang) > 1:
        return {lang: f['format_id'] for lang, f in best_audio_by_lang.items()}
    
    return {}

def download_audio_tracks(url, tracks_dict, download_dir='downloads'):
    """
    Downloads the audio tracks provided in tracks_dict as MP3 files.
    """
    os.makedirs(download_dir, exist_ok=True)
    for lang, format_id in tracks_dict.items():
        print(f"\n -> Downloading '{lang}' audio track...")
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(download_dir, f'%(title)s_audio_{lang}.%(ext)s'),
            'nocheckcertificate': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"    ✅ Done: {lang} track saved.")
        except Exception as e:
            print(f"    ❌ Error downloading {lang} track: {e}")