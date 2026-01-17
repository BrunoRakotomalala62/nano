from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Config
API_KEY = "sk-YPnScysOGcvoVpshC99966Df24Cc46C7BdEfD48dC56a97A2"
BASE_URL = "https://api.laozhang.ai/v1/chat/completions"

@app.route('/api', methods=['GET'])
def generate():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    payload = {
        "model": "claude-3-5-sonnet-latest", # Switching to a Claude model as GPT-4o failed in test
        "messages": [{"role": "user", "content": prompt}]
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
