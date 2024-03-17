from langchain.retrievers import ContextualCompressionRetriever, CohereRagRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.chat_models import ChatCohere
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
import os, dotenv

user_query = "When was Cohere started?"
dotenv.load_dotenv()
API_KEY_OK = os.getenv('COHERE_API_KEY')

# Create cohere's chat model and embeddings objects
cohere_chat_model = ChatCohere(cohere_api_key=API_KEY_OK)
cohere_embeddings = CohereEmbeddings(cohere_api_key=API_KEY_OK)

# Load text files and split into chunks, you can also use data gathered elsewhere in your application
raw_documents = TextLoader('D:\code\shlokathon\intellectquest\\backend\\test.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# Create a vector store from the documents
db = Chroma.from_documents(documents, cohere_embeddings)
input_docs = db.as_retriever().get_relevant_documents(user_query)

# Create the cohere rag retriever using the chat model 
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