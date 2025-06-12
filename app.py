import streamlit as st
import os
import shutil
import subprocess
import json
import pandas as pd
from generate_email import generate_outreach_email

HTML_DIR = "html_outputs"
PARSED_DIR = "parsed_json"

def clear_previous_outputs():
    if os.path.exists(HTML_DIR):
        shutil.rmtree(HTML_DIR)
    if os.path.exists(PARSED_DIR):
        shutil.rmtree(PARSED_DIR)
    os.makedirs(HTML_DIR, exist_ok=True)
    os.makedirs(PARSED_DIR, exist_ok=True)

def run_scrape(industry, count):
    result = subprocess.run(["python", "scrape.py", industry, str(count)], capture_output=True, text=True)
    if result.returncode != 0:
        st.error("Scrape failed:\n\n" + result.stderr)
        return False
    return True

def run_parse():
    result = subprocess.run(["python", "parse.py"], capture_output=True, text=True)
    if result.returncode != 0:
        st.error("Parse failed:\n\n" + result.stderr)
        return False
    return True

def load_parsed_results():
    files = [f for f in os.listdir(PARSED_DIR) if f.endswith(".json")]
    data = []
    for f in files:
        with open(os.path.join(PARSED_DIR, f), "r", encoding="utf-8") as infile:
            try:
                obj = json.load(infile)
                tf = obj.get("total_funding", "")
                if isinstance(tf, str) and len(tf) % 2 == 0 and tf[:len(tf)//2] == tf[len(tf)//2:]:
                    obj["total_funding"] = tf[:len(tf)//2]
                if isinstance(obj.get("key_people"), list):
                    obj["key_people"] = [
                        f"{p.get('name', '')} ({p.get('title', '')})" if isinstance(p, dict) else str(p)
                        for p in obj["key_people"]
                    ]
                obj["__filename"] = f
                data.append(obj)
            except Exception as e:
                st.warning(f"⚠ Failed to load {f}: {e}")
    return data

def get_news_for_company(company_name):
    result = subprocess.run(["python", "pipeline.py", company_name], capture_output=True, text=True)
    if result.returncode != 0:
        return None, f"Failed to run pipeline.py: {result.stderr}"
    try:
        with open("company_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("news", []), None
    except Exception as e:
        return None, str(e)

def generate_email_for_company(company_name):
    try:
        with open("company_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        summary = data.get("news_summary", "")
        email = generate_outreach_email(company_name, summary)
        return email.strip(), None
    except Exception as e:
        return None, str(e)

# --- UI ---
st.set_page_config("Crunchbase Scraper", layout="wide")
st.title("Crunchbase Scraper & Parser")

industry = st.text_input("Industry Tag", value="")
count = st.number_input("Number of Companies", min_value=1, max_value=50, value=5, step=1)

if st.button("Run Scrape + Parse"):
    clear_previous_outputs()
    with st.spinner("Scraping Crunchbase..."):
        if run_scrape(industry, count):
            with st.spinner("Parsing HTML files..."):
                if run_parse():
                    st.success("Scraping and parsing complete!")

data = load_parsed_results()
if data:
    st.subheader("Parsed Company Data")

    df = pd.DataFrame(data).drop(columns=["__filename"], errors="ignore")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.markdown("### Interact with Companies")

    for i, company in enumerate(data):
        name = company.get("name", f"Company {i+1}")
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.markdown(f"**{name}**")

        news_key = f"news_data_{i}"
        email_key = f"email_data_{i}"

        if col2.button("📰 Get News", key=f"news-{i}"):
            news, err = get_news_for_company(name)
            if err:
                st.error(err)
            elif news:
                st.session_state[news_key] = news
            else:
                st.warning("No news found.")

        if news_key in st.session_state:
            with st.expander(f"🗞 News for {name}", expanded=True):
                for item in st.session_state[news_key]:
                    st.markdown(f"- [{item['title']}]({item['url']}) ({item['date']} • {item['source']})")

        if col3.button("✉️ Generate Email", key=f"email-{i}"):
            email, err = generate_email_for_company(name)
            if err:
                st.error(err)
            elif email:
                st.session_state[email_key] = email
            else:
                st.warning("Could not generate email.")

        if email_key in st.session_state:
            with st.expander(f"📬 Outreach Email for {name}", expanded=True):
                st.code(st.session_state[email_key])
else:
    st.info("Run a scrape first to see company data.")
