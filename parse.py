import os
import json
import json5
import re
import requests
from bs4 import BeautifulSoup

# Groq API details
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Directories
HTML_DIR = "html_outputs"
OUTPUT_DIR = "parsed_json"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Prompt template
PROMPT_TEMPLATE = """
Extract structured company information from the following Crunchbase HTML. 
Respond only with a valid JSON object (no preamble or explanation).

Required fields:
- name (string)
- description (string)
- website (string)
- location (string)
- founded_year (integer)
- employee_count (string)
- total_funding (string)
- last_funding_type (string)
- last_funding_date (string)
- investors (array of strings)
- key_people (array of strings with titles)
- tech_stack (array of strings)
- industry (string)

---HTML START---
{text}
---HTML END---

Respond ONLY with a valid JSON object.
"""

def call_groq(prompt):
    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI that extracts structured company data from HTML."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 2048
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=HEADERS, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"GROQ API Error: {response.status_code} - {response.text}")

def clean_groq_response(response: str) -> str:
    # Strip triple backtick markdown
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()

    # Remove trailing commas before closing braces/brackets
    response = re.sub(r",\s*([\]}])", r"\1", response)

    return response

def parse_response_to_json(response: str, filename: str):
    cleaned = clean_groq_response(response)
    try:
        return json.loads(cleaned), "valid"
    except json.JSONDecodeError:
        try:
            return json5.loads(cleaned), "auto-fixed (json5)"
        except Exception:
            print(f"Still invalid JSON after cleaning: {filename}")
            return response, "invalid"

def load_html_files(directory=HTML_DIR, max_length=8000):
    files = [f for f in os.listdir(directory) if f.endswith(".html")]
    for file in files:
        with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r"\n+", "\n", text)
            yield file, text[:max_length]

def main():
    if not os.path.exists(HTML_DIR):
        print(f"Directory '{HTML_DIR}' not found. Please run scrape.py first.")
        return

    html_files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]
    if not html_files:
        print(f"No HTML files found in '{HTML_DIR}'. Please run scrape.py first.")
        return

    print(f"Found {len(html_files)} HTML files to parse...")

    for filename, content in load_html_files():
        print(f"Parsing {filename}...")
        prompt = PROMPT_TEMPLATE.format(text=content)

        try:
            response = call_groq(prompt)

            parsed, status = parse_response_to_json(response, filename)

            company_name = filename.replace(".html", "")
            output_path = os.path.join(OUTPUT_DIR, f"{company_name}.json")
            raw_path = os.path.join(OUTPUT_DIR, f"{company_name}_raw.txt")

            with open(raw_path, "w", encoding="utf-8") as raw_file:
                raw_file.write(response)

            with open(output_path, "w", encoding="utf-8") as out_file:
                if isinstance(parsed, dict):
                    json.dump(parsed, out_file, indent=2)
                else:
                    out_file.write(parsed)

            print(f"Saved parsed result to {output_path} [{status}]")
        except Exception as e:
            print(f"Failed to parse {filename}: {str(e)}")

if __name__ == "__main__":
    main()
