import requests
import json

# Set the API endpoint
url = "http://localhost:1234/v1/completions"
headers = {
    "Content-Type": "application/json",
}

# Define the completion-based prompt
prompt = {
    "model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",  # Replace with the actual model ID, if required
    "prompt": "Explain quantum computing in simple terms.",
    "max_tokens": 100,
    "temperature": 0.7,
    "top_p": 0.9,
    "n": 1
}

# Send the request to the LLM model
response = requests.post(url, headers=headers, data=json.dumps(prompt))

# Parse the JSON response
if response.status_code == 200:
    result = response.json()
    print("Model response:", result['choices'][0]['text'])
else:
    print(f"Error: {response.status_code} - {response.text}")
