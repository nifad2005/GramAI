from flask import Flask,request,jsonify
from flask_cors import CORS
import json
import os
from google import genai
from model import load_chunks_and_index, query_in_data

client = genai.Client(api_key="AIzaSyAZL96CxSBUJaHjm-OufgMEL1KZHmd7Mxw")




app = Flask(__name__)
CORS(app)


def read_continuous_file(file_path):
    with open("constitution.pdf") as file:
        content = file.read()
    return content

def load_answers():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'answers.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#! Get request from user and give answer based on the input
@app.route('/get_answer', methods=['POST'])
def get_answer():
    request_data = request.get_json()
    question = request_data.get('question')
    chunks, index = load_chunks_and_index()

    response = query_in_data(question, index, chunks)
    return jsonify({'answer': response})


@app.route('/')
def index():
    return "Welcome to the backend server!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
# This code creates a simple Flask server that listens for POST requests on the /get_answer endpoint.