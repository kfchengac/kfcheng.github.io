# COLLIDE AI Lead Generation Tool

Automated lead discovery, qualification, and outreach for creative entrepreneurs.

## Features

- **Multi-Platform Search**: Instagram, LinkedIn, email databases
- **Smart Qualification**: Score leads based on followers, engagement, industry fit
- **Email Finding**: Integrate Hunter.io or pattern-based email discovery
- **Personalized Outreach**: Auto-generate custom messages per platform
- **Campaign Management**: Track, log, and export results
- **CRM Export**: Export qualified leads to CSV for import

## Setup

### 1. Install Dependencies

```bash
pip install requests python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Email (Gmail example - enable App Password in Google Account)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Hunter.io for email finding (optional)
HUNTER_API_KEY=your-hunter-io-key

# LinkedIn API (optional - requires Sales Navigator or API access)
LINKEDIN_ACCESS_TOKEN=your-linkedin-token

# OpenAI for enhanced personalization (optional)
OPENAI_API_KEY=your-openai-key
```

### 3. Run Lead Generation

```bash
python lead_gen.py
```

## Usage

### Basic Campaign

```python
from lead_gen import LeadGenerator

generator = LeadGenerator()

# Define search criteria
instagram_hashtags = ['#sustainablefashion', '#cleanbeauty', '#luxuryskincare']
linkedin_keywords = ['fashion brand founder', 'beauty brand CEO']

# Run campaign
results = generator.run_lead_generation_campaign(
    instagram_hashtags=instagram_hashtags,
    linkedin_keywords=linkedin_keywords,
    max_leads=100,
    auto_outreach=False  # Set True to auto-send
)
```

### Custom Qualification

```python
# Adjust qualification criteria
generator.lead_qualification_criteria = {
    'min_followers': 5000,
    'has_website': True,
    'engagement_rate': 3.0,
    'recent_activity': 30
}
```

### Manual Outreach

```python
# Generate message for a specific lead
lead = {
    'name': 'Sarah Chen',
    'company': 'Sustainable Beauty Co',
    'industry': 'beauty',
    'website': 'sustainablebeautyco.com'
}

message = generator.generate_personalized_message(lead, channel='email')
print(message['subject'])
print(message['body'])
```

### Export Leads

```python
# Export to CSV for CRM
generator.export_to_csv(qualified_leads, 'qualified_leads.csv')
```

## Platform Integration

### Instagram

- Uses hashtag search to find creative entrepreneurs
- Filters by follower count, engagement, bio keywords
- Requires Instagram Graph API access or careful scraping (respect ToS)

### LinkedIn

- Searches by job title, industry, company keywords
- Finds founders, CEOs, creative directors
- Requires LinkedIn API or Sales Navigator access

### Email Discovery

- Hunter.io integration for verified email addresses
- Pattern-based guessing for common formats
- Email validation before sending

## Outreach Channels

### Email

- Personalized subject lines
- Industry-specific value propositions
- Clear CTAs (15-min call, free brand audit, AI advisor access)
- Professional HTML formatting

### LinkedIn InMail

- Concise, value-focused messages
- Connection requests with personalized notes
- Engagement with posts before outreach

### Instagram DM

- Casual, authentic tone
- Visual-first approach
- Link to AI advisor tool
- Follow before messaging for higher response

## Lead Scoring System

Qualification score (0-100):

- **30 points**: 10K+ followers
- **20 points**: 5K-10K followers  
- **10 points**: 1K-5K followers
- **15 points**: Has website
- **15 points**: Founder/CEO title
- **10 points**: Target industry match
- **15 points**: High engagement (3%+)
- **10 points**: Active posting

**Qualified threshold**: 50+ points

## Campaign Workflow

1. **Search**: Scan multiple platforms with targeted keywords/hashtags
2. **Qualify**: Score each lead on business potential and fit
3. **Enrich**: Find email addresses and additional contact info
4. **Personalize**: Generate custom outreach messages
5. **Outreach**: Send via email, LinkedIn, or Instagram
6. **Track**: Log responses and engagement
7. **Export**: Save qualified leads to CRM

## Sample Output

```
🎨 COLLIDE AI - Lead Generation Campaign
============================================================

🔍 Searching Instagram with hashtags: ['#sustainablefashion', ...]
✅ Found 25 potential leads on Instagram

🔍 Searching LinkedIn with keywords: ['fashion brand founder', ...]
✅ Found 18 potential leads on LinkedIn

📊 Total leads found: 43

🎯 Qualifying leads...
✅ Sarah Chen - Score: 75
✅ Emily Rodriguez - Score: 68
✅ Marcus Johnson - Score: 62

✨ Qualified leads: 12/43

📧 Finding email addresses...
✉️  Sarah Chen: sarah@sustainablebeautyco.com
✉️  Emily Rodriguez: emily@lumierelifestyle.com

💾 Results saved to: leads_campaign_20251016_120000.json

📈 CAMPAIGN SUMMARY
============================================================
Total Leads Found: 43
Qualified Leads: 12
Outreach Sent: 0

🏆 TOP 5 LEADS:

1. Sarah Chen - Score: 75
   Platform: instagram
   Industry: beauty
   Reasons: Strong following (15,000), Has website, In beauty industry, High engagement (3.5%)
   Email: sarah@sustainablebeautyco.com
```

## Best Practices

### Do's
- Personalize every message with specific observations
- Research leads before reaching out
- Provide immediate value (insights, free audit, resources)
- Follow up 2-3 times with added value
- Track all interactions in CRM
- Test different message variations
- Respect platform rate limits and ToS

### Don'ts
- Spam or mass-message without personalization
- Use aggressive sales language
- Ignore opt-outs or unsubscribes
- Scrape data in violation of platform policies
- Send attachments in first contact
- Make false claims about your service

## Rate Limits

- **Email**: Max 50-100/day from new domain (warm up gradually)
- **LinkedIn**: Max 20-30 connection requests/day, 50-80 InMails/month
- **Instagram**: Max 20-30 DMs/day to avoid shadowban
- **Hunter.io**: API limits vary by plan (50-500 requests/month free tier)

## Compliance

- **CAN-SPAM**: Include unsubscribe link, physical address, honest subject
- **GDPR**: Obtain consent, provide data access/deletion
- **Platform ToS**: Respect automation policies, avoid scraping violations
- **Opt-out**: Honor all unsubscribe requests immediately

## Advanced Features

### A/B Testing

```python
# Test different subject lines
variants = [
    "Elevate {company}'s Brand Strategy",
    "Quick Question About {company}",
    "{name}, Here's a Free Brand Audit"
]

# Track open/response rates per variant
```

### Drip Campaigns

```python
# Multi-touch sequence
follow_ups = [
    {'day': 0, 'template': 'initial_outreach'},
    {'day': 3, 'template': 'value_add_resource'},
    {'day': 7, 'template': 'case_study_share'},
    {'day': 14, 'template': 'final_check_in'}
]
```

### Lead Enrichment

```python
# Add Clearbit, LinkedIn Sales Nav, or other data sources
# Enrich with company size, funding, tech stack, etc.
```

## Integration with COLLIDE AI Platform

- Auto-send AI advisor access to qualified leads
- Track which leads engage with the chat advisor
- Score leads by conversation depth and topics
- Prioritize warm leads for human follow-up
- Feed conversation data into CRM

## Troubleshooting

**No emails found**
- Add Hunter.io API key for verified addresses
- Use company website to guess common patterns
- Try LinkedIn profile email if public

**Low qualification scores**
- Adjust criteria thresholds
- Expand target industries/titles
- Search different hashtags/keywords

**Email bounces**
- Validate emails before sending
- Use email verification service
- Check for typos in domain

**Low response rates**
- Test different subject lines
- Shorten message length
- Add more specific personalization
- Improve value proposition
- Follow up with additional value

## License

Proprietary - COLLIDE AI Platform
