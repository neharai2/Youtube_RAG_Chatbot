
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def create_documents(transcript: str, video_id: str):

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    # Create LangChain documents
    documents = [
        Document(
            page_content=transcript,
            metadata={"video_id": video_id}
        )
    ]

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    return chunks
