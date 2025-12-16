# Lead Generation Tool - Quick Start Guide

## 📋 Overview

The COLLIDE AI Lead Generation tool automatically finds, qualifies, and reaches out to creative entrepreneurs across multiple platforms.

## 🚀 Quick Start

### 1. Install Additional Dependencies

```bash
cd ~/Documents/collide-ai-platform
pip3 install python-dotenv
```

### 2. Configure Your Credentials

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add:

```bash
# Email credentials (use Gmail App Password)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Optional: Hunter.io for email discovery
HUNTER_API_KEY=your-hunter-key

# Optional: LinkedIn API token
LINKEDIN_ACCESS_TOKEN=your-linkedin-token

# Optional: OpenAI for enhanced personalization
OPENAI_API_KEY=your-openai-key
```

### 3. Run Your First Campaign

```bash
python3 lead_gen.py
```

This will:
- Search Instagram and LinkedIn for creative entrepreneurs
- Score and qualify leads based on followers, engagement, industry fit
- Find email addresses
- Generate personalized outreach messages
- Save results to JSON file

## 📧 Gmail Setup (for outreach)

1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Account → Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character password
4. Use this password in `.env` as `EMAIL_PASSWORD`

## 🎯 Campaign Customization

Edit `lead_gen.py` to customize:

```python
# Target industries
target_industries = ['fashion', 'beauty', 'lifestyle', 'design']

# Qualification criteria
min_followers = 1000
min_engagement_rate = 2.0
min_score_threshold = 50

# Search terms
instagram_hashtags = ['#sustainablefashion', '#cleanbeauty']
linkedin_keywords = ['fashion brand founder', 'beauty brand CEO']
```

## 📊 Understanding Lead Scores

Leads are scored 0-100 based on:

- **Follower Count** (0-30 points)
  - 10K+: 30 points
  - 5K-10K: 20 points
  - 1K-5K: 10 points

- **Website Presence** (15 points)
- **Founder/CEO Title** (15 points)
- **Industry Match** (10 points)
- **High Engagement** (0-15 points)
- **Active Posting** (10 points)

**Qualified leads**: 50+ points

## 🔄 Automated Campaigns

Set `auto_outreach=True` to automatically send emails to qualified leads:

```python
results = generator.run_lead_generation_campaign(
    instagram_hashtags=['#sustainablefashion'],
    linkedin_keywords=['fashion brand founder'],
    max_leads=100,
    auto_outreach=True  # Enable auto-send
)
```

**Warning**: Start with `auto_outreach=False` and manually review messages before enabling automation.

## 📈 Results & Export

Campaign results are saved to:
- `leads_campaign_YYYYMMDD_HHMMSS.json` - Full campaign data
- Export to CSV: `generator.export_to_csv(leads, 'leads.csv')`

## 🌐 Web Interface (Optional)

Access the lead gen tool via web interface at:

```
http://localhost:5003/lead-gen
```

Features:
- Visual campaign builder
- Real-time lead table
- One-click outreach
- CSV export

## 🔐 API Integrations

### Hunter.io (Email Finding)
- Sign up: https://hunter.io
- Free tier: 50 searches/month
- Add key to `.env`: `HUNTER_API_KEY=xxx`

### LinkedIn API
- Requires LinkedIn Developer account
- Or use Sales Navigator for manual export
- Add token to `.env`: `LINKEDIN_ACCESS_TOKEN=xxx`

### Instagram Graph API
- Requires Facebook Developer account
- Business/Creator account needed
- Alternative: Manual search + export

## 📝 Best Practices

### Do's ✅
- Personalize every message with specific observations
- Provide immediate value (free audit, insights)
- Test subject lines and message variants
- Track responses in CRM
- Respect opt-outs immediately
- Warm up new email domains gradually (10-20/day first week)

### Don'ts ❌
- Mass-send generic messages
- Scrape platforms in violation of ToS
- Ignore rate limits (email: 50-100/day, LinkedIn: 20-30/day)
- Include attachments in first contact
- Use aggressive sales language

## 🎨 Integration with COLLIDE AI Platform

Lead gen integrates with the main platform:

1. **Automatic AI Advisor Access**: Send qualified leads access to the chat advisor
2. **Conversation Tracking**: See which leads engage with the AI
3. **Lead Scoring**: Rank by conversation depth and interest
4. **CRM Sync**: Export to your CRM of choice

## 🆘 Troubleshooting

**"Email authentication failed"**
- Check Gmail App Password (not regular password)
- Verify 2FA is enabled
- Try regenerating App Password

**"No emails found"**
- Add Hunter.io API key
- Check website URLs are correct
- Use pattern-based guessing as fallback

**"Low qualification scores"**
- Lower `min_score_threshold` (try 40)
- Adjust follower minimums
- Expand industry keywords

**"Rate limit exceeded"**
- Reduce max_leads parameter
- Add delays between requests
- Use platform API quotas wisely

## 📚 Advanced Usage

### Multi-Channel Campaigns

```python
# Email + LinkedIn + Instagram
campaign = {
    'email': generate_email_message(lead),
    'linkedin': generate_linkedin_message(lead),
    'instagram': generate_instagram_dm(lead)
}

# Send across all channels with delays
```

### A/B Testing

```python
# Test different subject lines
subjects = [
    "Quick question about {company}",
    "Elevate {company}'s brand strategy",
    "Free brand audit for {company}"
]

# Track which performs best
```

### Drip Sequences

```python
# Multi-touch follow-up
sequence = [
    {'day': 0, 'message': 'initial_outreach'},
    {'day': 3, 'message': 'value_add_resource'},
    {'day': 7, 'message': 'case_study_share'}
]
```

## 📞 Support

For questions or issues:
- Check LEAD_GEN_README.md for detailed documentation
- Review sample campaigns in lead_gen.py
- Contact: support@collideartistry.com

---

Built with ❤️ for COLLIDE AI Platform
