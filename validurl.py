from urllib.parse import urlparse

def is_valid_youtube_url(url: str) -> bool:
    """
    Checks if the provided URL is a valid YouTube URL.
    """
    if not url:
        return False
        
    # Add scheme if missing so urlparse can correctly identify the domain (netloc)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove 'www.' prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        valid_domains = [
            'youtube.com',
            'youtu.be',
            'm.youtube.com',
            'music.youtube.com',
            'youtube-nocookie.com'
        ]
        
        return domain in valid_domains
    except Exception:
        return False
