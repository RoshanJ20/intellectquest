from flask import Flask, render_template, request, jsonify
from google.generativeai import GenerativeModel
import google.generativeai as genai
from PyPDF2 import PdfReader
from collections import defaultdict
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


# Configure GenerativeAI
genai.configure(api_key='AIzaSyBPg0laQNUvgK87b5Y_bYjJZUUG0zBIVYg')
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

    # Split the response text into individual questions
    result = response.text.split('\n\n')
    print(result)
    # Iterate through each question and extract the question and options
    global questions

    global answer_key
    global concepts

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
            pdf_file_path = "C:/Users/Pratheesh/Desktop/Operating Systems Support.pdf"
        elif selected_module == "Module 2":
            pdf_file_path = "C:/Users/Pratheesh/Desktop/Operating Systems Support.pdf"
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

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    selected_answers = data.get('selected_answers', {})
    print("selected_answers: ",selected_answers)

    def get_option_letter(text):
        start_index = text.find("(") + 1  # Skip the opening parenthesis
        end_index = text.rfind(")")  # Use rfind for the last closing parenthesis
        if start_index != -1 and end_index != -1 and start_index < end_index:
            option_letter = text[start_index].strip()  # Extract and strip leading/trailing spaces
            if option_letter.isalpha() and len(option_letter) == 1:  # Check for single letter
                return option_letter
        return None

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
        option_letter = get_option_letter(text)
        if option_letter:
            sel.append(option_letter)
    ans=add_first_alphabet_to_list(answer_key)
    print(sel, ans)
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
        # Return a response indicating success or any relevant data
    return jsonify({"message": "Verification successful", "selected_options": dict(selected_answers)})
@app.route('/results', methods=['GET'])
def results():
    # Assume summary_data is defined and contains valid JSON data
    summary_data = {
        "labels": ["Correct", "Incorrect"],
        "values": na,
        "colors": ["Blue", "Red"]
    }

    # Render the template with the summary_data
    return render_template('results.html', summary_data=summary_data, cor_ans=cor_ans, topic=topic)

if __name__ == '__main__':
    app.run(debug=True)