from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)


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
