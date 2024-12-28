from langchain_community.document_loaders.firecrawl import FireCrawlLoader
from dotenv import load_dotenv, find_dotenv
import os
from utils.logger import setup_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv(find_dotenv())

firecrawl_api_key = os.environ.get("FIRECRAWL_API_KEY")

logger = setup_logger(__name__)

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

def firecrawl_handler_scrape(url):
    loader = FireCrawlLoader(
        api_key=firecrawl_api_key, url=url, mode="scrape" #Mode can change from 'scrape', 'crawl' or 'map'
    )

    docs = []
    for doc in loader.lazy_load():
        docs.append(doc)

    if docs:
        split_docs = splitter.split_documents(docs)

        logger.info(f"Found URL for scraping")
        logger.info(f"Splitting documents into {len(split_docs)} chunks")

        return split_docs
    