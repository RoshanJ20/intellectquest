from langchain_community.vectorstores import SupabaseVectorStore
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from supabase.client import Client, create_client
import dotenv, os
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
import os, dotenv
import cohere
import re
from flask import Flask, request, jsonify
from flask_cors import CORS


dotenv.load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


app = Flask(__name__)
CORS(app)

API_KEY_OK = os.getenv('COHERE_API_KEY')
cohere_chat_model = ChatCohere(cohere_api_key=API_KEY_OK)
cohere_embeddings = CohereEmbeddings(cohere_api_key=API_KEY_OK)
co = cohere.Client(os.getenv('COHERE_API_KEY'))

vector_store = SupabaseVectorStore(
    embedding=cohere_embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
)
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('userInput')
    matched_docs = vector_store.similarity_search(user_input)
    page_content = matched_docs[0].page_content
    sections = re.split(r'\n-{2,}\n', page_content)
    docs = []
    for section in sections:
        lines = section.strip().split('\n')
        title = lines[0].strip()
        snippet = '\n'.join(lines[1:]).strip()
        docs.append({"title": title, "snippet": snippet})

    response = co.chat(
            message=user_input,
            documents = docs
            )
    print(response.text)
    return jsonify({"message": response.text})

if __name__ == '__main__':
    app.run(debug=True)