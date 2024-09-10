# gemini_integration.py
import os
from google.generative_ai import GoogleGenerativeAI

api_key = "AIzaSyAi4RcPWCz6gP2dff23o65fXoi4a_9lXek" #os.getenv("GEMINI_API_KEY")
gen_ai = GoogleGenerativeAI(api_key)
model = gen_ai.get_model("gemini-1.5-flash")

def generate_response(prompt):
    try:
        result = model.generate_content(prompt)
        response_text = result['candidates'][0]['output'] if result['candidates'] else "No response generated."
        return response_text
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Error generating content."
