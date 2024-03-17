from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)



# def chat():
#     data = request.json
#     user_input = data.get('userInput')

#     try:
#         # Simplified OpenAI call for GPT-4
#         response = client.completions.create(model="gpt-3.5-turbo-1106",  # Adjust model as needed
#         prompt={user_input},
#         max_tokens=150)

#         # Assuming a single text response; adjust as necessary
#         text_response = response.choices[0].text.strip()

#         return jsonify({"message": text_response})
#     except Exception as e:
#         print(e)
#         return jsonify({"error": "Error processing your request"}), 500



import cohere

co = cohere.Client(os.getenv('COHERE_API_KEY'))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('userInput')
    try:
        response = co.chat(
        message=user_input)
        print(response.text)
        return jsonify({"message": response.text})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True)
