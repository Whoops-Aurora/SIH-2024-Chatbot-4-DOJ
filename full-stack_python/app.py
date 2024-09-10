from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import re
import nltk
from nltk.tokenize import sent_tokenize

# Download necessary NLTK data
nltk.download('punkt')

# Initialize Flask app
app = Flask(__name__)

# Set up Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

def clean_text(text):
    """Removes emojis and invalid characters from text."""
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    cleaned_text = emoji_pattern.sub(r'', text)
    return re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)

def chunk_text(text, chunk_size=1000):
    """Splits text into smaller chunks."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

@app.route('/')
def index():
    """Renders the main chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handles user chat input and returns a response from Gemini API."""
    data = request.get_json()
    user_input = data.get('question', '')

    if user_input:
        # Start a chat session and send the message to the Gemini model
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        
        # Print the entire response object for debugging
        print("Response Object:", response)
        
        # Access the response text properly - now checking for 'content' instead of 'text'
        if response.candidates and len(response.candidates) > 0:
            # Trying to access the 'content' field instead of 'text'
            return jsonify({'response': response.candidates[0].content})
        else:
            return jsonify({'response': 'No valid response from model'}), 400
    return jsonify({'response': 'Invalid input'}), 400

@app.route('/api/chunk', methods=['POST'])
def chunk():
    """Receives a text file, cleans it, and chunks the text."""
    data = request.get_json()
    text = data.get('text', '')
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)
    return jsonify({'chunks': chunks})

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file upload, cleaning, and chunking."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        text = file.read().decode('utf-8')
        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)
        return jsonify({'chunks': chunks})
    return jsonify({'error': 'File processing error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
