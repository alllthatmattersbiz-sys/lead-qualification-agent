# 🤖 AI Automation Lead Qualifier

An intelligent lead discovery and qualification tool that finds AI/Automation opportunities from **HackerNews** and **GitHub**, analyzes them with **Claude AI**, and saves qualified leads to **Google Sheets**.

---

## ✨ Features

- 🔍 **Multi-Source Scraping** - Find leads from HackerNews and GitHub
- 🤖 **Claude AI Qualification** - Intelligent scoring (1-10) with AI analysis
- 📧 **Email Draft Generation** - AI-generated personalized outreach emails
- 💾 **Google Sheets Export** - Automatically save qualified leads
- 🎯 **Customizable** - Choose how many leads to qualify (1-10)
- ⚡ **Cost-Effective** - Uses Claude Haiku (~$0.001 per lead)

---

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/alllthatmattersbiz-sys/lead-qualification-agent.git
cd lead-qualification-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure
Create `.env`:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_SHEET_ID=your_sheet_id
```

Add `google_credentials.json` (downloaded from Google Cloud)

### 3. Run
```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## 📊 How It Works

```
HackerNews + GitHub
        ↓
    Search for Leads
        ↓
  Claude Analyzes
        ↓
   Generate Scores
        ↓
   Draft Emails
        ↓
  Save to Google Sheets
```

---

## 🎯 Usage

1. **Select sources** (HackerNews, GitHub)
2. **Click "Search Sources"** → Finds all leads
3. **Choose how many to qualify** (1-10)
4. **Click "Qualify X Leads"** → Claude analyzes each
5. **Review results** → See scores & email drafts
6. **Click "Save to Sheets"** → Export to Google Sheets

---

## 💰 Cost Breakdown

- Claude Haiku: **$0.001 per lead qualified**
- 10 leads = ~$0.01
- 100 leads = ~$0.10
- Google Sheets: Free
- HackerNews/GitHub APIs: Free

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **AI:** Claude API (Haiku)
- **Lead Sources:** HackerNews API, GitHub API
- **Data Export:** Google Sheets API
- **Language:** Python 3.11+

---

## 📁 Project Structure

```
lead-qualification-agent/
├── app.py                    # Main Streamlit app
├── sources/
│   ├── hackernews.py        # HackerNews scraper
│   └── github.py            # GitHub scraper
├── processors/
│   ├── claude_qualifier.py  # Claude AI qualification
│   └── sheets_handler.py    # Google Sheets integration
├── requirements.txt
├── .env                     # (Don't commit!)
├── google_credentials.json  # (Don't commit!)
└── README.md
```

---

## 🔧 Configuration

### Environment Variables
```
ANTHROPIC_API_KEY          # Your Claude API key (sk-ant-...)
GOOGLE_SHEET_ID            # Your Google Sheet ID
```

### Customize Search Keywords

Edit `sources/hackernews.py`:
```python
keywords = [
    "AI automation",
    "AI engineer",
    "AI consultant",
    "machine learning"
]
```

---

## 📈 Output Example

Each qualified lead includes:

| Field | Example |
|-------|---------|
| Score | 8/10 |
| Status | ✅ Qualified |
| Author | John Doe |
| Company | TechStartup Inc |
| Opportunity | Need AI chatbot built |
| Budget | $10k-20k |
| Timeline | 2 weeks |
| Email Subject | "AI chatbot solution for your support" |
| Email Opening | "Hi John, I saw your post..." |

---

## 🚀 Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repo
5. Add secrets: `ANTHROPIC_API_KEY`, `GOOGLE_SHEET_ID`
6. Deploy!

Your app will be live at: `https://lead-qualification-agent-xxx.streamlit.app`

---

## ⚠️ Important

### API Keys
- **Never commit** `.env` or `google_credentials.json`
- Use `.gitignore` to protect secrets
- Use Streamlit Cloud Secrets for deployed apps

### Rate Limits
- GitHub: 60 requests/hour (unauthenticated)
- Claude: Check your Anthropic plan
- Google Sheets: Unlimited

### Best Practices
1. Verify leads independently before outreach
2. Personalize emails based on AI drafts
3. Start with 1-2 qualifications to test
4. Monitor your Claude API usage

---

## 🤝 What's Next?

### Planned Features
- [ ] Reddit scraping (r/forhire)
- [ ] Email sending integration
- [ ] Lead filtering & sorting
- [ ] Historical analytics
- [ ] Slack notifications

---

## 📚 Resources

- [Claude API](https://docs.anthropic.com)
- [Streamlit](https://docs.streamlit.io)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [GitHub API](https://docs.github.com/en/rest)

---

## 📄 License

MIT License

---

**Built with ❤️ for founders & freelancers**

*v1.0 - April 2026*