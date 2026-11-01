
from src.transcript import get_transcript, extract_video_id

# Test YouTube URL
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

try:
    video_id = extract_video_id(youtube_url)
    print("Video ID:", video_id)

    transcript = get_transcript(youtube_url)

    print("\nTranscript extracted successfully!")
    print("\nFirst 500 characters:")
    print(transcript[:500])

    print("\nTotal characters:", len(transcript))

except Exception as e:
    print("Error:", str(e))
