
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def create_vector_store(documents):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    return vector_store


def save_vector_store(vector_store, path="vector_db"):

    vector_store.save_local(path)

    print(f"Vector store saved at: {path}")


def search_vector_store(vector_store, query, k=3):

    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return results


def load_vector_store(path="vector_db"):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vector_store = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store
