
from src.transcript import get_transcript, extract_video_id
from src.document_processor import create_documents

youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Step 1: Extract transcript
video_id = extract_video_id(youtube_url)
transcript = get_transcript(youtube_url)

# Step 2: Create chunks
chunks = create_documents(transcript, video_id)

# Step 3: Display results
print("Video ID:", video_id)
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)
