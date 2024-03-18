from langchain.retrievers import ContextualCompressionRetriever, CohereRagRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
import os, dotenv

user_query = "What is a Linked List?"
dotenv.load_dotenv()
API_KEY_OK = os.getenv('COHERE_API_KEY')

# Create cohere's chat model and embeddings objects
cohere_chat_model = ChatCohere(cohere_api_key=API_KEY_OK)
cohere_embeddings = CohereEmbeddings(cohere_api_key=API_KEY_OK)

persist_directory = 'db'

vectordb = Chroma(persist_directory=persist_directory, embedding_function=cohere_embeddings)
input_docs = vectordb.as_retriever().get_relevant_documents(user_query)

rag = CohereRagRetriever(llm=cohere_chat_model)
docs = rag.get_relevant_documents(
    user_query,
    source_documents=input_docs,
)
# Print the documents
for doc in docs[:-1]:
    print(doc.metadata)
    print("\n\n" + doc.page_content)
    print("\n\n" + "-" * 30 + "\n\n")
# Print the final generation 
answer = docs[-1].page_content
print(answer)
# Print the final citations 
citations = docs[-1].metadata['citations']
print(citations)