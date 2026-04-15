from flask import Flask, render_template, request, jsonify

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def generate_grocery_list(query):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Return only a comma-separated list of grocery items for the given dish. Do not include introductory text."},
                {"role": "user", "content": query}
            ]
        )
        ai_message = completion.choices[0].message.content
        # Split by comma and clean up whitespace
        return [item.strip() for item in ai_message.split(',')]
    
    except Exception as e:
        print(f"Error calling Groq: {e}")
        return [f"Error: Could not connect to AI. {str(e)}"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-grocery", methods=["POST"])
def get_grocery():
    user_input = request.json.get("query")

    if not user_input:
        return jsonify(["Please enter a dish name!"])

    result = generate_grocery_list(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


