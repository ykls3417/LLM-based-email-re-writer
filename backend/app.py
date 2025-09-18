from flask import Flask, request, jsonify, send_from_directory
from typing import Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import json
import datetime
import re

# Initialize Flask app with static folder pointing to React build
app = Flask(__name__, static_folder="../frontend/build", static_url_path="")

# Load environment variables
load_dotenv(find_dotenv())

class EmailRewriter:
    def __init__(self, model="deepseek/deepseek-chat-v3-0324:free", user_apikey=None, base_url="https://openrouter.ai/api/v1"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=user_apikey if user_apikey else os.getenv('OPENROUTER_API_KEY'),
        )
        self.model = model

    def rewrite(self, email_text: str, reason: str, other_instruction: str) -> Dict[str, Any]:
        # Basic preprocessing: Check for time-sensitive keywords
        time_keywords = re.compile(
            r'\b('
            r'today|tomorrow|next week|this year|yesterday|'
            r'\d{1,2}/\d{1,2}/\d{2,4}|'
            r'\d{4}-\d{1,2}-\d{1,2}|'
            r'january|february|march|april|may|june|july|august|september|october|november|december|'
            r'jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec|'
            r'\b\d{4}\b|'
            r'\b\d{1,2}(st|nd|rd|th)?\b'
            r')\b',
            re.IGNORECASE
        )
        has_time_refs = bool(time_keywords.search(email_text + reason + other_instruction))
        if has_time_refs:
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            other_instruction += f"\n- Ensure all temporal references align with the current date: {current_date}, and carefully identify if the event in content happened before or after current time."

        # Prepare the prompt (unchanged)
        prompt = f"""You are a professional email rewriter, expert in crafting clear, effective emails for various audiences.

**Context**: You are given:
- Original email text: 
{email_text}
- Brief reason for the email: 
{reason}
- User instructions: 
{other_instruction}

**Objective**: Rewrite the email to fulfill the user's instructions, preserving all key facts, dates, and requests from the original. Improve clarity, grammar, and structure. If subject, recipient, or sender are not explicit in the inputs, infer or generate suitable ones based on the content and reason. If information seems outdated or unavailable, avoid speculating and note in the caution field (e.g., 'Based on available information as of current date, the [placeholder] have not been filled'). If anything in the email is unsure or made up by you, which you have to remind user, you must note in the caution field.

**Style**: Keep it concise, professional, and error-free. Use standard email formatting (e.g., greeting, body paragraphs, closing).

**Tone**: Default to polite and formal; adjust based on audience (e.g., warmer for colleagues, neutral for clients, respectful for academic professionals) or user instructions.

**Audience**: Infer from the reason or instructions (e.g., business, personal). Assume professional if unclear. Use inclusive, culturally neutral language.

**Response**: Output ONLY valid JSON in this exact format, no extra text:
{{
    "subject": "Email subject",
    "recipient": "Recipient name or email",
    "sender": "Sender name or email",
    "body": "Full email body including greeting and sign-off",
    "caution": "Any caution or reminder about the email that user should know"
}}
"""

        # API call with retry logic
        max_retries = 5
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    extra_body={},
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = completion.choices[0].message.content.strip()
                content = content.replace('```json\n', '').replace('\n```', '').replace('```', '')
                parsed_response = json.loads(content)
                print(f"INPUT PROMPT:\n{prompt}\n\nOUTPUT PARSED RESULT:\n{json.dumps(parsed_response, indent=2)}")
                return parsed_response
            except Exception as e:
                error_type = type(e).__name__
                error_msg = f"{error_type}: {str(e)}"
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt} failed: API call or JSON parse failed: {error_msg}")
                    continue
                raw_response = content if 'content' in locals() else None
                return {
                    "error": f"API call or JSON parse failed: {error_msg}",
                    "raw_response": raw_response
                }

# Serve React frontend for all non-API routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/rewrite', methods=['POST'])
def rewrite_email():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        reason = data.get('reason', '')
        email_text = data.get('email_text', '')
        instruction = data.get('instruction', '')
        user_model = data.get('model')
        user_api_key = data.get('api_key')
        user_base_url = data.get('base_url')
        
        if not all([reason, email_text, instruction]):
            return jsonify({"error": "Missing required fields: reason, email_text, instruction"}), 400
        
        rewriter = EmailRewriter(
            model=user_model if user_model else "deepseek/deepseek-chat-v3-0324:free",
            user_apikey=user_api_key if user_api_key else None,
            base_url=user_base_url if user_base_url else "https://openrouter.ai/api/v1"
        )
        result = rewriter.rewrite(email_text, reason, instruction)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))