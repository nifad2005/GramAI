from flask import Flask,request,jsonify
from flask_cors import CORS
import json
import os
from google import genai

client = genai.Client(api_key="AIzaSyAZL96CxSBUJaHjm-OufgMEL1KZHmd7Mxw")




app = Flask(__name__)
CORS(app)

def load_answers():
    json_path = os.path.join(os.path.dirname(__file__), 'data', 'answers.json')
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#! Get request from user and give answer based on the input
@app.route('/get_answer', methods=['POST'])
def get_answer():
    user_input = request.json.get('question').strip()
   
    # answers={
    #     "hello": "হ্যালো! কিভাবে সাহায্য করতে পারি?",
    #     "জমি সংক্রান্ত": "জমি সংক্রান্ত সমস্যার জন্য স্থানীয় ভূমি অফিসে যোগাযোগ করুন।",
    #     "বৈবাহিক": "বৈবাহিক সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
    #     "আর্থিক": "আর্থিক সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
    #     "অন্যান্য": "অন্যান্য সমস্যার জন্য স্থানীয় সমাজসেবা অফিসে যোগাযোগ করুন।",
    # }
    
    # # answers = load_answers()
    # answer = answers.get(user_input, "দুঃখিত, আমি আপনার প্রশ্নের উত্তর জানি না।")

    instruction = """
        তুমি একজন দক্ষ আইন সহায়ক এজেন্ট, যার কাজ শুধুমাত্র বাংলাদেশের আইন সম্পর্কিত প্রশ্নের উত্তর দেওয়া।
        যদি প্রশ্নটি আইন সম্পর্কিত না হয়, তাহলে বলো:
        'দুঃখিত, আমি শুধু আইন সম্পর্কিত প্রশ্নের উত্তর দিতে পারি।'
        
        তোমাকে চেষ্টা করতে হবে উত্তরকে যথা সম্ভব সংক্ষিপ্ত এবং সহজ ভাষায় দিতে।

        প্রশ্ন:
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents= instruction + user_input
    )


    # print(response.output_text)


    return jsonify({'answer': response.text})


@app.route('/')
def index():
    return "Welcome to the backend server!"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
# This code creates a simple Flask server that listens for POST requests on the /get_answer endpoint.