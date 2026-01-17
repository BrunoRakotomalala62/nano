import requests
import os
import json
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Config
API_KEY = "sk-YPnScysOGcvoVpshC99966Df24Cc46C7BdEfD48dC56a97A2"
BASE_URL = "https://api.laozhang.ai/v1/chat/completions"
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            uid TEXT PRIMARY KEY,
            history JSONB
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

def get_history(uid):
    if not uid: return []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT history FROM chat_history WHERE uid = %s', (uid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else []

def save_history(uid, history):
    if not uid: return
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO chat_history (uid, history) VALUES (%s, %s)
        ON CONFLICT (uid) DO UPDATE SET history = EXCLUDED.history
    ''', (uid, json.dumps(history)))
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api', methods=['GET'])
def generate():
    prompt = request.args.get('prompt')
    model = request.args.get('model', 'claude-3-5-sonnet-latest')
    image_url = request.args.get('image')
    uid = request.args.get('uid')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    history = get_history(uid)
    
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
            save_history(uid, history)
        
        return jsonify({
            "auteur": "Bruno",
            "content": content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gemini', methods=['GET'])
def gemini():
    return generate() # Use the main generate logic for gemini as well to maintain history

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
