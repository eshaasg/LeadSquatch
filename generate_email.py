import os
import json
import requests

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_outreach_email(company_name, news_summary):
    prompt = f"""
You are a sales outreach assistant.

Write only the subject line and outreach email body (no extra commentary) to the team at {company_name}, based on this company update summary:

\"\"\"{news_summary}\"\"\"

Make it concise, human, professional, and proactive. Keep it under 150 words. Return only the subject and the body.
"""

    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who drafts professional business outreach emails."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 300
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=HEADERS, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"GROQ API Error: {response.status_code} - {response.text}")
