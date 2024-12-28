from uuid import uuid4
from dotenv import load_dotenv, find_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
import time
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from utils.logger import setup_logger

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "multi-agent-for-laws" 

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)

embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')

def compile_pinecone_docs(docs):
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    uuids = [str(uuid4()) for _ in range(len(docs))]

    logger.info("ADDING DOCUMENTS TO PINECONE")

    vector_store.add_documents(documents=docs, ids=uuids)

def return_pinecone_retriever():
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    logger.info("GENERATING A PINECONE RETRIEVER")

    retriever = vector_store.as_retriever(
        search_type="mmr",
    )

    return retriever