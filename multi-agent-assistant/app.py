import os
from flask import Flask, request, jsonify
import google.generativeai as genai

# Import the tools (sub-agents) we built
from tools import add_task, get_pending_tasks, save_note

app = Flask(__name__)

# Configure Gemini API using the environment variable method you mastered in Track 1
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Initialize the Primary Agent with our Tool functions
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[add_task, get_pending_tasks, save_note]
)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online", 
        "agent": "Multi-Agent Coordinator",
        "message": "Send a POST request to /execute with a 'prompt' key."
    }), 200

@app.route('/execute', methods=['POST'])
def execute_task():
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "Please provide a 'prompt' in the JSON payload"}), 400
        
    user_prompt = data['prompt']
    
    try:
        # Start a chat session with automatic function calling enabled.
        # This allows the Manager Agent to perform multi-step workflows automatically.
        chat = model.start_chat(enable_automatic_function_calling=True)
        
        # Send the user's request. The agent will handle tool execution behind the scenes!
        response = chat.send_message(user_prompt)
        
        return jsonify({
            "status": "success",
            "input": user_prompt,
            "response": response.text
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)