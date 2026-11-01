
from src.vector_store import load_vector_store
from src.rag_pipeline import (
    create_rag_pipeline,
    ask_question
)

# Step 1: Load existing FAISS database
print("Loading vector database...")

vector_store = load_vector_store()

print("Vector database loaded successfully!")

# Step 2: Create RAG pipeline
retriever, rag_chain = create_rag_pipeline(vector_store)

print("RAG pipeline initialized!")

# Step 3: Ask a question
question = "What does the singer promise?"

print("\nQuestion:", question)

# Step 4: Generate answer
answer, source_documents = ask_question(
    retriever,
    rag_chain,
    question
)

print("\nAI Answer:")
print(answer)

# Step 5: Display retrieved sources
print("\nRetrieved Sources:")

for i, document in enumerate(source_documents):

    print(f"\nSource {i + 1}:")
    print(document.page_content[:200])
    print("Metadata:", document.metadata)
