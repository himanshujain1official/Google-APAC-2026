import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 1. Configuration: Grab the API key from environment variables (Required for Cloud Run)
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    # Fallback for local testing only. Remove or leave blank for production!
    API_KEY = "YOUR_LOCAL_TESTING_API_KEY" 

genai.configure(api_key=API_KEY)

# 2. Initialization: Using Flash for speed and efficiency
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 3. The HTTP Endpoint: The hackathon requires the agent to be callable
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online", 
        "agent": "ADK Summarizer", 
        "message": "Send a POST request to /summarize with a JSON payload containing a 'text' field."
    }), 200
@app.route('/summarize', methods=['POST'])
def summarize_text():
    try:
        # Parse the incoming JSON payload
        data = request.get_json()
        
        # Extract the 'text' field. Default to empty string if missing.
        text_to_summarize = data.get('text', '')

        if not text_to_summarize:
            return jsonify({"error": "Please provide 'text' in your JSON payload."}), 400

        # Create the system instruction/prompt
        prompt = f"You are an expert summarization agent. Concisely summarize the following text:\n\n{text_to_summarize}"
        
        # --- ADK INTEGRATION NOTE ---
        # If the hackathon requires a specific Agent Development Kit (ADK) class wrapper 
        # instead of direct generation, replace the line below with your ADK syntax.
        # ----------------------------
        response = model.generate_content(prompt)
        
        # Return the valid response
        return jsonify({
            "agent_name": "Summarizer-Agent",
            "status": "success",
            "summary": response.text
        }), 200

    except Exception as e:
        return jsonify({"error": f"Agent execution failed: {str(e)}"}), 500

# 4. Server Execution
if __name__ == '__main__':
    # Cloud Run dynamically assigns a port via the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)