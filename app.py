from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
import json
import openai

app=Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']= 'Content-Type'

@app.route("/status")
def status():
    return jsonify({"status":"ok"})

@app.route("/bot",methods = ['POST','GET'])
def bot():
    openai.api_key = json.load(open("env.json"))["OPENAI_API_KEY"]
    req_data = request.get_json()
    user_message = req_data['user_message']
    prompt=f"""You are an helpful Assistant who can provide answers to User's questions.\n
            User: "Who is Bill Gates?\n
            Assistant: Bill Gates is an American business magnate, software developer, investor, and philanthropist. He is best known as the co-founder of Microsoft Corporation. Gates has held the Forbes title of the richest person in the world multiple times, and is currently the second-richest person in the world according to Forbes.\n
            User: "What is Reactjs?\n
            Assistant: Reactjs is an open-source JavaScript library for building user interfaces. It is maintained by Facebook and a community of individual developers and corporations. React can be used as a base in the development of single-page or mobile applications.\n
            User: {user_message}\n
            Assistant:"""

    final_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt = prompt,
        temperature=0.7,
        max_tokens=500,
        top_p=0.1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(final_response["choices"][0]["text"])
    response = {
        'final_response': final_response["choices"][0]["text"],
        'status': "sucessful",
    }
    
    return jsonify(response)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)

