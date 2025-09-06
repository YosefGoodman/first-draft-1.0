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

#Initialize Local Database 
import sqlite3  
import json  
  
def init_database():  
    conn = sqlite3.connect('chatbot_memory.db')  
    cursor = conn.cursor()  
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS conversations (  
            id INTEGER PRIMARY KEY,  
            user_input TEXT,  
            context TEXT,  
            response TEXT,  
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  
        )  
    ''')  
    conn.commit()  
    return conn
#end

#Define get_response Function 
def get_response(self, user_input):  
    # i. Check local memory for context  
    context = self.get_context_from_db(user_input)  
      
    try:  
        # ii. Send input + context to OpenAI API  
        response = self.client.chat.completions.create(  
            model="gpt-3.5-turbo",  
            messages=[  
                {"role": "system", "content": context},  
                {"role": "user", "content": user_input}  
            ]  
        )  
        result = response.choices[0].message.content  
          
    except Exception as e:  
        # iii. If API fails, use fallback logic  
        result = self.fallback_response(user_input)  
      
    # iv. Return formatted response  
    self.save_to_db(user_input, context, result)  
    return self.format_response(result)
#end


#Define get_multi_response Function 
async def get_multi_response(self, user_input):  
    # Query multiple LLM APIs concurrently  
    responses = await asyncio.gather(  
        self.query_openai(user_input),  
        self.query_claude(user_input),  
        self.query_llama(user_input),  
        self.query_mistral(user_input),  
        return_exceptions=True  
    )  
      
    # Filter successful responses  
    valid_responses = [r for r in responses if not isinstance(r, Exception)]  
      
    # Aggregate and rank responses  
    best_response = self.select_best_response(valid_responses)  
      
    return self.format_response(best_response)  
  
def select_best_response(self, responses):  
    # Implement logic to score and select best response  
    # Could use factors like: length, confidence, relevance, etc.  
    return max(responses, key=lambda x: self.score_response(x))
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

