from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from typing import Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

class EmailRewriter:
    def __init__(self, model="deepseek/deepseek-chat-v3-0324:free", temperature=0.7, max_tokens=120, provider="auto", token=None):
        load_dotenv(find_dotenv())
        self.client = client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY'),
        )
        self.model = model

    def rewrite(self, email_text: str, reason: str, other_instruction: str) -> Dict[str, Any]:
        completion = self.client.chat.completions.create(
            extra_body={},
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                "role": "user",
                "content": f"""You are a professional email rewriter. You are professional in writing emails to different audiences. Your task is to rewrite the provided email in a suitable tone for the audience, and return in proper JSON format. 
                
                You are provided with the email text, a brief reason for the email, and some instruction from the user. You need to rewrite it in a professional tone with completing the instruction from the user, and output it in the following JSON output format.

                OUTPUT FORMAT:
                {{
                    "subject": "The subject of the email",
                    "recipient": "The recipient of the email",
                    "sender": "The sender of the email",
                    "date": "The date of the email",
                    "body": "The body of the email"
                }}
                
                Below is the brief reason for the email: {reason}
                Below are the email text: {email_text}
                Below is the instrcution from the user: {other_instruction}"""
                }
            ]
        )
        try:
            content = completion.choices[0].message.content
            
            # Try to parse as JSON, if it fails return the raw content
            try:
                content = content.replace('```json\n', '').replace('\n```', '').strip()
                return json.loads(content)
            except json.JSONDecodeError:
                return {"error": "Failed to parse response", "raw_content": content}
        except Exception as e:
            return {"error": str(e)}

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/api/rewrite', methods=['POST'])
def rewrite_email():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        reason = data.get('reason', '')
        email_text = data.get('email_text', '')
        instruction = data.get('instruction', '')
        
        if not all([reason, email_text, instruction]):
            return jsonify({"error": "Missing required fields: reason, email_text, instruction"}), 400
        
        rewriter = EmailRewriter()
        result = rewriter.rewrite(email_text, reason, instruction)
        
        print(result)

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
