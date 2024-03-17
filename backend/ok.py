from langchain_community.chat_models import ChatCohere
from langchain_core.messages import AIMessage, HumanMessage
import os, dotenv

dotenv.load_dotenv()

cohere_chat_model = ChatCohere(cohere_api_key=os.getenv('COHERE_API_KEY'))

# Send a chat message without chat history
current_message = [HumanMessage(content="knock knock")]
print(cohere_chat_model(current_message))

# Send a chat message with chat history, note the last message is the current user message
current_message_and_history = [
    HumanMessage(content="knock knock"),
    AIMessage(content="Who's there?"),
    HumanMessage(content="Tank") ]
print(cohere_chat_model(current_message_and_history))