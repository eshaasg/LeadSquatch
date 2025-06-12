# LeadSquatch 🦈

A powerful lead generation tool that scrapes Crunchbase based on industry tags and delivers comprehensive company intelligence with automated outreach capabilities.

# Overview 🛰️

LeadSquatch employs a sophisticated multi-stage pipeline that:
1. **Industry Scraper**: Discovers companies by industry tags using Crunchbase search
2. **Data Extractor**: Pulls comprehensive company data including funding, team, and tech stack
3. **News Intelligence**: Aggregates and summarizes recent company news using AI
4. **Outreach Generator**: Creates personalized email templates based on latest company updates

The result is a complete lead generation solution that provides actionable company intelligence with ready-to-send outreach emails.

# How it works 🚀
### Initial Build
Started with a web scraping architecture using SeleniumBase to navigate Crunchbase's dynamic content and extract comprehensive company profiles.

### Data Collection
Leveraged intelligent HTML parsing and JSON extraction to retrieve detailed company information including funding history, employee data, technology stack, and leadership team.

### AI Integration 
Integrated Groq's Llama3-70B model for structured data extraction and BART-large-CNN for news summarization, enabling intelligent processing of raw company data.

### News Intelligence
Implemented automated news aggregation and summarization to provide timely insights about target companies for more relevant outreach.

### Outreach Automation
Built AI-powered email generation that creates personalized outreach messages based on recent company news and developments.

### Performance

Speed: 5-8s for company discovery, 10-15s for complete data extraction

Impact: Cuts lead research time by ~80% and outreach preparation by ~70%

# How to run it 🛠️
### 1. Install dependencies
   ```bash
   pip install -r requirements.txt
```

### 2. Install Ollama 
 Download from [here](https://ollama.com/download) if you prefer local processing
   ```bash
    ollama pull phi
```

### 3. Set up API keys
 The tool uses Groq API for AI processing. Update the API keys in .env:
   ```python
    GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Usage
#### Discover companies by industry:
```bash
python scrape.py "fintech" 10
```

#### Extract single company data:
```bash
python pipeline.py "company-name"
```

#### Run frontend:
```bash
streamlit run app.py
```

# Features ✨

### Smart News Intelligence
- Finds and summarizes the latest company news automatically
- Spots perfect timing opportunities for your outreach

### Outreach That Actually Works
- Writes personalized emails based on what's happening at each company
- Creates subject lines that get opened, not ignored

### Deep Company Insights
- Pulls everything you need: funding rounds, team size, tech stack
- Gives you conversation starters beyond the basic company info

### Built to Scale
- Process dozens of companies in one go
- Handles errors gracefully so you don't lose your work

# Video Demo  

### [YouTube🔗]([https://youtu.be/ljXnd5LBorU](https://youtu.be/4KpwePUu66Y))

# Screenshots

![image](https://github.com/user-attachments/assets/1888cc09-9ec1-4099-b38d-2f7f6161982b)

![image](https://github.com/user-attachments/assets/aa259d1e-6a69-48c7-ba30-f0e7a5bcf98e)

![image](https://github.com/user-attachments/assets/7daf49e5-6aa1-4eed-ae14-5c5e84592b95)

![image](https://github.com/user-attachments/assets/26764051-3878-400a-afa9-2bfe4a82651b)




