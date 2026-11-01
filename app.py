
import streamlit as st

from src.transcript import get_transcript, extract_video_id
from src.document_processor import create_documents
from src.vector_store import create_vector_store, save_vector_store
from src.rag_pipeline import create_rag_pipeline, ask_question


# --------------------------------
# 1. Page Configuration
# --------------------------------

st.set_page_config(
    page_title="YouTube AI Assistant",
    page_icon="🎥",
    layout="wide"
)


# --------------------------------
# 2. Initialize Session State
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False

if "video_id" not in st.session_state:
    st.session_state.video_id = None


# --------------------------------
# 3. Application Header
# --------------------------------

st.title("🎥 YouTube AI Assistant")

st.caption(
    "Ask questions and understand YouTube videos using AI."
)

st.divider()


# --------------------------------
# 4. Sidebar - Video Processing
# --------------------------------

with st.sidebar:

    st.header("📹 Video Configuration")

    youtube_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    if st.button("🚀 Process Video", use_container_width=True):

        if not youtube_url.strip():

            st.warning("Please enter a YouTube URL.")

        else:

            # Reset previous video state
            st.session_state.video_processed = False
            st.session_state.retriever = None
            st.session_state.rag_chain = None
            st.session_state.messages = []

            try:

                with st.spinner("Processing YouTube video..."):

                    # Step 1: Extract video ID
                    video_id = extract_video_id(youtube_url)

                    # Step 2: Extract transcript
                    transcript = get_transcript(youtube_url)

                    if not transcript.strip():
                        raise ValueError(
                            "The video transcript is empty."
                        )

                    # Step 3: Create document chunks
                    documents = create_documents(
                        transcript,
                        video_id
                    )

                    # Step 4: Generate embeddings and create FAISS
                    vector_store = create_vector_store(documents)

                    # Step 5: Save vector database
                    save_vector_store(vector_store)

                    # Step 6: Initialize RAG pipeline
                    retriever, rag_chain = create_rag_pipeline(
                        vector_store
                    )

                    # Step 7: Save objects in session state
                    st.session_state.retriever = retriever
                    st.session_state.rag_chain = rag_chain
                    st.session_state.video_id = video_id
                    st.session_state.video_processed = True

                st.success("Video processed successfully!")

            except Exception as e:

                st.error(f"Error processing video: {str(e)}")

    if st.session_state.video_processed:

        st.success("✅ Video is ready for questions")

        st.caption(
            f"Video ID: {st.session_state.video_id}"
        )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []


# --------------------------------
# 5. Main Chat Interface
# --------------------------------

st.subheader("💬 Chat with your video")

if not st.session_state.video_processed:

    st.info(
        "Please enter a YouTube URL in the sidebar "
        "and click Process Video to get started."
    )


# --------------------------------
# 6. Display Chat History
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("sources"):

            with st.expander("View retrieved sources"):

                for i, source in enumerate(
                    message["sources"], start=1
                ):

                    st.markdown(f"**Source {i}**")
                    st.write(source)


# --------------------------------
# 7. User Chat Input
# --------------------------------

if st.session_state.video_processed:

    if prompt := st.chat_input(
        "Ask something about your video..."
    ):

        # Display user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate RAG response
        with st.chat_message("assistant"):

            try:

                with st.spinner("Thinking..."):

                    answer, source_documents = ask_question(
                        st.session_state.retriever,
                        st.session_state.rag_chain,
                        prompt
                    )

                st.markdown(answer)

                # Display retrieved sources
                sources = [
                    document.page_content
                    for document in source_documents
                ]

                with st.expander("View retrieved sources"):

                    for i, source in enumerate(
                        sources, start=1
                    ):

                        st.markdown(f"**Source {i}**")
                        st.write(source)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:

                error_message = f"Unable to generate answer: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
