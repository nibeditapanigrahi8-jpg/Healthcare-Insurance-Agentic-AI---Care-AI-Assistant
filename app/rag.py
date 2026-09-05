from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB_PATH = str(BASE_DIR / "chroma_db")
POLICY_FILE = str(BASE_DIR / "data" / "careplus_policy.txt")

def create_vectorstore():

    loader = TextLoader(
        POLICY_FILE
    )

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        documents
    )

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    return vectorstore

def get_vectorstore():

    if not os.path.exists(VECTOR_DB_PATH):
        return create_vectorstore()

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

    return vectorstore


def get_retriever():

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

"""if __name__ == "__main__":

    create_vectorstore()

    print("Vector database created successfully.")"""
#python app/rag.py