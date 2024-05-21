import os
import openai
from supabase.client import Client, create_client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

supabase_url = os.environ['DB_URL']
supabase_key = os.environ['DB_KEY']
openai.api_key = os.environ['OPENAI_API_KEY']

supabase: Client = create_client(supabase_url, supabase_key)
embeddings = OpenAIEmbeddings()

# Create the vector store
vector_store = SupabaseVectorStore(
    client=supabase,
    table_name='documents',
    embedding=embeddings,
)

def perform_similarity_search(query_vector, top_k=5):

    # Perform similarity search
    results = vector_store.similarity_search(query_vector, k=top_k)
    results = [r.page_content for r in results]
    return results

def ask_gpt(query, context):
    messages = [
        {
            "role": "system",
            "content": "You are an expert computer scientist and can help solve all programming, coding, or technology. You answer in step-by-step answers that are simple to understand but still detailed and correctly answer the question"
        },
        {
            "role": "user",
            "content": query,
        },
        {
            "role": "assistant",
            "content": '\n\n'.join(context),
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        # max_tokens=400,  
        temperature=0.4,  
    )
    print("Assistant's Response:")
    print(response['choices'][0]['message']['content'])

def ask(query):
    context = perform_similarity_search(query)
    ask_gpt(query, context)

if __name__ == "__main__":
    query = input("Enter the query here, or q to quit: ")
    
    while query != "q":
        ask(query)
        print("")
        query = input("Enter the query here, or q to quit: ")


