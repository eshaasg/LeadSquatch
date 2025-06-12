import os
import json
import time
import sys
from seleniumbase import SB
from bs4 import BeautifulSoup
import re

OUTPUT_DIR = "html_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DISCOVER_URL = "https://www.crunchbase.com/discover/organization.companies"

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def get_company_links(sb, industry_tag, max_count):
    sb.open(DISCOVER_URL)
    sb.wait_for_ready_state_complete()
    sb.sleep(3)

    # Accept cookies if prompted
    sb.click_if_visible("#onetrust-accept-btn-handler", timeout=5)

    # Type search query
    search_input = 'input[placeholder*="Search"]'
    sb.wait_for_element_visible(search_input, timeout=10)
    sb.type(search_input, industry_tag + "\n")
    sb.sleep(4)

    # Scroll to load companies
    for _ in range(5):
        sb.scroll_to_bottom()
        sb.sleep(2)

    # Scrape company profile links
    links = set()
    for a in sb.find_elements("a[href*='/organization/']"):
        href = a.get_attribute("href")
        if "/organization/" in href:
            links.add(href.split("?")[0])
        if len(links) >= max_count:
            break

    return list(links)[:max_count]

def save_html(sb, url):
    sb.open(url)
    sb.wait_for_ready_state_complete()
    sb.sleep(5)
    sb.click_if_visible("#onetrust-accept-btn-handler", timeout=3)
    company_name = url.rstrip("/").split("/")[-1]
    filename = sanitize_filename(company_name) + ".html"
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(sb.get_page_source())
    print(f"Saved: {filename}")

def main():
    # Check if arguments are provided via command line
    if len(sys.argv) == 3:
        industry_tag = sys.argv[1]
        max_count = int(sys.argv[2])
    # Check if environment variables are set (for Streamlit integration)
    elif os.getenv("INDUSTRY_TAG") and os.getenv("MAX_COMPANIES"):
        industry_tag = os.getenv("INDUSTRY_TAG")
        max_count = int(os.getenv("MAX_COMPANIES"))
    else:
        # Fallback to input prompts
        industry_tag = input("Enter an industry tag to search: ")
        max_count = int(input("How many companies to scrape? "))

    print(f"\n Searching Crunchbase for: {industry_tag}\n")

    with SB(uc=True, headless=True, locale="en") as sb:
        try:
            links = get_company_links(sb, industry_tag, max_count)
            print(f"Found {len(links)} company links")
            for url in links:
                save_html(sb, url)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()