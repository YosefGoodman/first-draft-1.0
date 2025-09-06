"""
app.py
-------
Main Flask application for the AI chatbot.

Instructions:
- Handles incoming HTTP requests to chat endpoint.
- Uses database.py for storing/retrieving conversation history.
- Uses multi_llm.py (if implemented) to handle multiple LLM responses.
- Loads API keys from api.env using python-dotenv.
- Add any fallback or error handling for API failures.
"""

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from database import init_db, get_recent_context, save_interaction
# from multi_llm import get_multi_response  # Uncomment if multi-LLM is implemented
import openai
 


#Connect to OpenAI API 
#import openai  
from openai import OpenAI  
  
class ChatbotCore:  
    def __init__(self, api_key):  
        self.client = OpenAI(api_key=api_key)
#end




# Load API key
load_dotenv("api.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize database
init_db()

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    """
    Endpoint for chatbot messages.
    Request JSON should contain:
        - user_id: unique user identifier
        - message: the user input
    Response JSON:
        - response: chatbot output
    """
    data = request.json
    user_id = data.get("user_id", "default")
    user_input = data.get("message", "")

    # Retrieve last few messages for context
    context = get_recent_context(user_id, limit=5)

    # Generate response (basic OpenAI call)
    prompt = "\n".join(context) + "\nUser: " + user_input
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        bot_response = response.choices[0].message.content
    except Exception:
        bot_response = "Sorry, I can't respond right now."

    # Save interaction in DB
    save_interaction(user_id, user_input, bot_response)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)

