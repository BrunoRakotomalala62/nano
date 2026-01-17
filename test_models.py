import requests
import json

API_KEY = "sk-YPnScysOGcvoVpshC99966Df24Cc46C7BdEfD48dC56a97A2"
BASE_URL = "https://api.laozhang.ai/v1/chat/completions"

# List extracted from the file
models = [
    "chatgpt-4o-latest", "claude-3-5-haiku-20241022", "claude-3-5-haiku-latest", 
    "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022", "claude-3-5-sonnet-latest", 
    "claude-3-7-sonnet-20250219", "claude-3-haiku-20240307", "claude-3-sonnet-20240229",
    "deepseek-chat", "deepseek-reasoner", "deepseek-v3", "gemini-1.5-pro-latest", 
    "gemini-2.0-flash-001", "gemini-2.5-flash", "gemini-2.5-flash-image", "gpt-4o", "gpt-4o-mini"
]

results = {}

print("Starting model connectivity tests...")

for model in models:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            results[model] = "Working"
            print(f"[SUCCESS] {model}")
        else:
            results[model] = f"Failed ({response.status_code})"
            print(f"[FAILED] {model}: {response.status_code}")
    except Exception as e:
        results[model] = f"Error: {str(e)}"
        print(f"[ERROR] {model}: {str(e)}")

with open("test_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\nTests complete. Results saved to test_results.json")
