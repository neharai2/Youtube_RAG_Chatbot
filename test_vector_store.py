
from src.transcript import get_transcript, extract_video_id
from src.document_processor import create_documents
from src.vector_store import (
    create_vector_store,
    save_vector_store,
    search_vector_store
)

# Step 1: Extract YouTube transcript
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

video_id = extract_video_id(youtube_url)
transcript = get_transcript(youtube_url)

print("Transcript extracted!")

# Step 2: Convert transcript into chunks
documents = create_documents(transcript, video_id)

print("Total chunks:", len(documents))

# Step 3: Generate embeddings and store in FAISS
vector_store = create_vector_store(documents)

print("Embeddings generated successfully!")

# Step 4: Save vector database
save_vector_store(vector_store)

# Step 5: Perform semantic search
query = "What does the singer say about love?"

results = search_vector_store(vector_store, query, k=3)

print("\nSearch Results:")

for i, result in enumerate(results):

    print(f"\nResult {i + 1}:")
    print(result.page_content)
    print("Metadata:", result.metadata)
