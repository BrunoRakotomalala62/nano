import requests
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
API_KEY = os.environ.get("API_KEY_LAOZHANG", "sk-YPnScysOGcvoVpshC99966Df24Cc46C7BdEfD48dC56a97A2")
BASE_URL = "https://api.laozhang.ai/v1/chat/completions"

# In-memory history (volatile - will reset on server restart)
chat_histories = {}

@app.route('/api', methods=['GET'])
def generate():
    prompt = request.args.get('prompt')
    model = request.args.get('model', 'claude-3-5-sonnet-latest')
    image_url = request.args.get('image')
    uid = request.args.get('uid')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Get or initialize history for this UID
    if uid not in chat_histories:
        chat_histories[uid] = []
    
    history = chat_histories[uid]
    
    # Construct the message content
    current_content = []
    if image_url:
        current_content.append({"type": "image_url", "image_url": {"url": image_url}})
    current_content.append({"type": "text", "text": prompt})
    
    history.append({"role": "user", "content": current_content})
    
    # Keep history manageable (last 10 messages)
    if len(history) > 10:
        history = history[-10:]

    payload = {
        "model": model,
        "messages": history
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(BASE_URL, json=payload, headers=headers)
        data = response.json()
        
        content = ""
        if 'choices' in data and len(data['choices']) > 0:
            content = data['choices'][0].get('message', {}).get('content', '')
            history.append({"role": "assistant", "content": content})
        
        return jsonify({
            "auteur": "Bruno",
            "content": content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gemini', methods=['GET'])
def gemini():
    return generate()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
