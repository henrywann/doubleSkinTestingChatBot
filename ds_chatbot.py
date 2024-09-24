# -*- coding: utf-8 -*-
"""ds_chatbot.py
Original file is located at
    https://colab.research.google.com/drive/1clg5HuXDaFHRI75uLK2KnYtVmXPli4dr
"""


from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_PASSWORD')



# Load the rules from the text file
with open('rules.txt', 'r', encoding='utf-8') as f:
    rules = f.read()


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')

    messages = [
        {"role": "system", "content": "你是一名游戏规则专家，以下是游戏规则。"},
        {"role": "system", "content": rules},
        {"role": "user", "content": f"请做两件事，先严格按照游戏规则回答问题：{question}；然后在回答的最后附上这句话：'详细游戏规则请参考playbook:https://docs.google.com/document/d/1nirsxRgRRGzFKZbhZx8dYH6FElr2rnLI3lqsO5vGeNE/edit?usp=sharing'"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # max_tokens=100,
        # temperature=0.5
    )

    answer = response['choices'][0]['message']['content'].strip()

    return jsonify({"answer": answer})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Heroku sets the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=True)
