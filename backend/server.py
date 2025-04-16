from flask import Flask,request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#! Get request from user and give answer based on the input
@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json.get('question').strip()
    print(f"Received input: {user_input}")
    answers={
        "hello": "হ্যালো! কিভাবে সাহায্য করতে পারি?",
        "জমি সংক্রান্ত": "জমি সংক্রান্ত সমস্যার জন্য স্থানীয় ভূমি অফিসে যোগাযোগ করুন।",
        "বৈবাহিক": "বৈবাহিক সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
        "আর্থিক": "আর্থিক সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
        "অন্যান্য": "অন্যান্য সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
    }
    answer = answers.get(user_input, "দুঃখিত, আমি আপনার প্রশ্নের উত্তর জানি না।")
    return jsonify({'answer': answer})


@app.route('/')
def index():
    return "Welcome to the backend server!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
# This code creates a simple Flask server that listens for POST requests on the /get_answer endpoint.