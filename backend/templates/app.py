from flask import Flask, render_template, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
from PyPDF2 import PdfReader
from collections import defaultdict
from flask_cors import CORS
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


# Configure GenerativeAI
genai.configure(api_key='AIzaSyAeZn2FoP4Kd0pFEQiyk8d7xd1vjjxBw0s')
answer_key=[]
questions = []
concepts=[]
na=[]
cor_ans=[]
topic=[]
# Function to read text from PDF file
def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Function to generate questions using GenerativeAI
def generate_questions(text):
    model = GenerativeModel('gemini-pro')
    response = model.generate_content(text+" From the above content can you generate 11 Questions from 11 different concepts with 4 options (3 Wrong options and 1 correct option) . Please send me the answer key separately with all the correct option (a or b or c) and at last give me Concepts List it is a list informing me from which Concepts the question was taken from")
    questions_with_options = []

    global questions
    global answer_key
    global concepts

    # Split the response text into individual questions
    result = response.text.split('\n\n')
    print(result)
    # Iterate through each question and extract the question and options
    current_section = None

    for item in result:
        if item.startswith("**Questions:**"):
            current_section = "questions"
        elif item.startswith("**Answer Key:**"):
            current_section = "answer_key"
        elif item.startswith("**Concepts List:**") or item.startswith("**Question Concepts:**"):
            current_section = "concepts"
        else:
            if current_section == "questions":
                split_item = item.split("\n")  # Split by double newlines
                if len(split_item) > 1:
                    question_text = split_item[0]
                    options = [opt.strip() for opt in split_item[1:5] if opt.strip()]
                    questions.append({"question": question_text, "options": options})
            elif current_section == "answer_key":
                answer_key.extend(item.split("\n"))
            elif current_section == "concepts":
                concepts.extend(item.split("\n"))

    if len(answer_key) > 11 and len(concepts) > 11 and len(generated_questions) > 11:
        answer_key = answer_key[-11:]
        concepts = concepts[-11:]
        questions = questions[-11:]

    print("Questions:", questions)
    print("Answer Key:", answer_key)
    print("Concepts:", concepts)
    return questions,concepts,answer_key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get selected module from dropdown
        selected_module = request.json['module']

        # Initialize variable to store the PDF file path
        pdf_file_path = ""

        # Determine the PDF file path based on the selected module
        if selected_module == "Module 1":
            pdf_file_path = "D:\code\shlokathon\intellectquest\\backend\\templates\\Arraye.pdf"
        elif selected_module == "Module 2":
            pdf_file_path = "D:\code\shlokathon\intellectquest\\backend\\templates\\Arraye.pdf"
        # Add more conditions for other modules if needed
        print(selected_module)
        # Check if a PDF file path is determined
        if pdf_file_path:
            # Read text from PDF
            pdf_text = read_pdf(pdf_file_path)
            # Generate questions from PDF text
            generated_questions, concepts, answer_key = generate_questions(pdf_text)
 
            # Render the questions.html template with the generated questions, concepts, and answer key
            return jsonify(questions=generated_questions, concepts=concepts,
                                   answer_key=answer_key)

    # If the request method is GET or no PDF file path is determined
    # Render the index.html template, which contains the form for selecting a module
    return render_template('index.html')


from collections import defaultdict

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

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    selected_answers = data.get('selected_answers', {})
    print("selected_answers: ",selected_answers)

    selected_options = {}
    for key, value in selected_answers.items():
        if value == "option0":
            selected_options[key] = 'a'
        elif value == "option1":
            selected_options[key] = 'b'
        elif value == "option2":
            selected_options[key] = 'c'
        elif value == "option3":
            selected_options[key] = 'd'

    selected_answers = selected_options

    def add_first_alphabet_to_list(strings):
        first_alphabets = []
        for string in strings:
            for char in string:
                if char.isalpha():
                    first_alphabets.append(char.lower())
                    break  # Stop searching once the first alphabet is found
        return first_alphabets
    
    ans = []
    global cor_ans
    global topic
    sel = []

    for text in selected_answers.values():
        if text:
            sel.append(text)
    
    print("answerkey",answer_key)
    ans=add_first_alphabet_to_list(answer_key)
    print("answerkey",ans)
    print('sel',sel)
    cor = []
    for i in range(len(sel)-1):
        if sel[i] == ans[i]:
            cor.append(1)
        else:
            cor_ans.append([questions[i]["question"],questions[i]["options"],ans[i]])
            topic.append(concepts[i])
            cor.append(0)
    print(cor)
    print(cor_ans)
    print(topic)
    global na
    na=[]
    na.append(cor.count(1))
    na.append(cor.count(0))
    print(na)

    summary_data = {
        "labels": ["Correct", "Incorrect"],
        "values": na,
        "colors": ["Blue", "Red"]
    }
    return jsonify(summary_data=summary_data, cor_ans=cor_ans, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)