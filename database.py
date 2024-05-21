from stackOverflow import scrape_post
import os
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
import json

supabase_url = os.environ['DB_URL']
supabase_key = os.environ['DB_KEY']

supabase: Client = create_client(supabase_url, supabase_key)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
embeddings = OpenAIEmbeddings()

# loading vector database
links = []
with open('links.json', 'r') as json_file:
    # Step 3: Parse the JSON content into a Python list
    links = json.load(json_file)

for i, link in enumerate(links):
    content = scrape_post(link)
    if content == "":
        continue
    print(f"Post {i}")

    docs = text_splitter.split_text(content)
    vector_store = SupabaseVectorStore.from_texts(docs, embeddings, client=supabase, table_name="documents", query_name="match_documents")
