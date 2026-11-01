from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url: str) -> str:
    parsed_url = urlparse(youtube_url)

    if parsed_url.hostname in ("youtu.be", "www.youtu.be"):
        return parsed_url.path.lstrip("/")

    if parsed_url.hostname in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com"
    ):
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query).get("v", [""])[0]

        if parsed_url.path.startswith(("/embed/", "/shorts/")):
            return parsed_url.path.split("/")[2]

    raise ValueError("Invalid YouTube URL")


def get_transcript(youtube_url: str) -> str:
    video_id = extract_video_id(youtube_url)

    youtube_api = YouTubeTranscriptApi()
    transcript = youtube_api.fetch(video_id)

    return " ".join(
        snippet.text for snippet in transcript
    )
