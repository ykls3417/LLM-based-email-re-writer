from typing import Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv,find_dotenv


class EmailRewriter:
    def __init__(self, model="deepseek/deepseek-chat-v3-0324:free", temperature=0.7, max_tokens=120, provider="auto", token=None):
        load_dotenv(find_dotenv())
        self.client = client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY'),
        )
        self.model = model

    def rewrite(self, email_text: str, reason: str) -> Dict[str, Any]:
        completion = self.client.chat.completions.create(
            # extra_headers={
            #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
            #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            # },
            extra_body={},
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {
                "role": "user",
                "content": f"""You are a professional email rewriter. You are professional in writing emails to different audiences. Your task is to rewrite the provided email in a suitable tone for the audience, and return in proper JSON format. 
                
                You are provided with the email text and a brief reason for the email, and you need to rewrite it in a professional tone and output it in the following JSON output format.

                OUTPUT FORMAT:
                {{
                    "subject": "The subject of the email",
                    "recipient": "The recipient of the email",
                    "sender": "The sender of the email",
                    "date": "The date of the email",
                    "body": "The body of the email"
                }}
                
                Below is the brief reason for the email: {reason}
                Below are the email text: {email_text}"""
                }
            ]
        )
        try:
            return completion.choices[0].message.content
        except Exception as e:
            print(e)
            return ""


def rewrite_email(reason, email_text, **kwargs):
    rewriter = EmailRewriter(**kwargs)
    return rewriter.rewrite(email_text, reason)


if __name__ == "__main__":
    # Simple example usage
    reason = "I, Marco Ho, as a student, want to have a quick meeting with the professor to discuss the project, on tmr afternoon."

    email_text = "Hi, can we meet tmrw? Thx!"
    
    print(rewrite_email(reason, email_text))