# 🔗 Real API Integration Guide for Lead Generation

This guide shows you how to connect your lead generation tool to **real Instagram and LinkedIn APIs** to find actual leads.

---

## 📱 Instagram API Setup

Instagram requires a Facebook Developer account and a Business/Creator Instagram account.

### Step 1: Create Facebook App

1. **Go to Facebook Developers**: https://developers.facebook.com/
2. **Create an App**:
   - Click "Create App"
   - Choose "Business" type
   - Fill in app details
   - Click "Create App"

### Step 2: Add Instagram Graph API

1. In your app dashboard, click **"Add Product"**
2. Find **"Instagram Graph API"** and click "Set Up"
3. Go to **Settings → Basic** and note your:
   - App ID
   - App Secret

### Step 3: Get Access Token

1. Go to **Tools → Graph API Explorer**
2. Select your app
3. Click "Generate Access Token"
4. Grant permissions:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_read_engagement`
5. **Copy the token** (it's temporary)

### Step 4: Get Long-Lived Token

Run this in terminal:
```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN"
```

### Step 5: Add to .env

```bash
INSTAGRAM_ACCESS_TOKEN=your-long-lived-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-account-id
```

### Limitations:
- ❌ Cannot search by hashtags (Instagram removed this in 2020)
- ✅ Can search your own tagged posts
- ✅ Can get user profiles via mentions
- 💡 **Alternative**: Use RapidAPI Instagram scrapers (see below)

---

## 💼 LinkedIn API Setup

LinkedIn has strict API access requirements. Here are **3 options**:

### Option 1: Official LinkedIn API (Requires Partnership)

**Requirements**:
- Company LinkedIn page
- Partnership agreement with LinkedIn
- Approval process (can take weeks/months)

**Steps**:
1. Go to: https://www.linkedin.com/developers/
2. Create an app
3. Apply for Marketing Developer Platform access
4. Wait for approval

### Option 2: RapidAPI LinkedIn Scraper (Recommended)

**Much easier - No partnership needed!**

1. **Sign up**: https://rapidapi.com/
2. **Find LinkedIn API**: Search "LinkedIn Scraper" or "LinkedIn Profile Data"
3. **Popular options**:
   - **Fresh LinkedIn Profile Data** (by Tomba.io)
   - **LinkedIn Data Scraper** (by ScraperAPI)
   - **LinkedIn Profile & Company Data** (by Contact Out)

4. **Subscribe** (free tier usually available)
5. **Get API Key** from dashboard
6. **Add to .env**:
   ```bash
   RAPIDAPI_KEY=your-rapid-api-key
   RAPIDAPI_LINKEDIN_HOST=linkedin-data-scraper.p.rapidapi.com
   ```

### Option 3: Phantombuster (Automation Tool)

1. Sign up: https://phantombuster.com/
2. Use "LinkedIn Search Export" phantom
3. Get API key
4. Automate searches

---

## 📧 Hunter.io Setup (Email Discovery)

**Easiest API to set up!**

1. **Sign up**: https://hunter.io/
2. **Free tier**: 50 searches/month
3. **Get API Key**: Dashboard → API → Copy key
4. **Add to .env**:
   ```bash
   HUNTER_API_KEY=your-hunter-api-key
   ```

**Usage**: Automatically finds email addresses from domain names (e.g., "example.com")

---

## 🚀 Quick Start: Instagram Scraping (Without Official API)

Since Instagram's official API is limited, here's a practical approach:

### Use Instagram Scraping Tools

#### Option A: RapidAPI Instagram Scrapers

1. **Sign up**: https://rapidapi.com/
2. **Search**: "Instagram Scraper"
3. **Recommended**:
   - **Instagram Scraper API** by Social Media Scraper
   - **Instagram Data API** by DataForSEO
   - **Instagram Looter** by Toolhouse

4. **Pricing**: Usually $0-10/month for 1000-10,000 requests

5. **Add to .env**:
   ```bash
   RAPIDAPI_KEY=your-rapid-api-key
   RAPIDAPI_INSTAGRAM_HOST=instagram-scraper-api2.p.rapidapi.com
   ```

#### Option B: Apify Instagram Scrapers

1. **Sign up**: https://apify.com/
2. **Find**: "Instagram Hashtag Scraper" or "Instagram Profile Scraper"
3. **Free tier**: $5 credit (good for ~5,000 profiles)
4. **Get API token**: Settings → Integrations → API tokens
5. **Add to .env**:
   ```bash
   APIFY_API_TOKEN=your-apify-token
   ```

---

## 🛠️ Updated .env File Template

After setting up your APIs, your `.env` should look like:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
PORT=8080
PUBLIC_URL=http://localhost:8080

# Email Configuration (for outreach)
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Instagram API (choose one)
# Option 1: Official Facebook/Instagram API (limited)
INSTAGRAM_ACCESS_TOKEN=your-instagram-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your-account-id

# Option 2: RapidAPI Instagram Scraper (recommended)
RAPIDAPI_KEY=your-rapidapi-key
RAPIDAPI_INSTAGRAM_HOST=instagram-scraper-api2.p.rapidapi.com

# Option 3: Apify Instagram Scraper
APIFY_API_TOKEN=your-apify-token

# LinkedIn API (choose one)
# Option 1: Official LinkedIn API (requires partnership)
LINKEDIN_ACCESS_TOKEN=your-linkedin-token

# Option 2: RapidAPI LinkedIn Scraper (recommended)
RAPIDAPI_LINKEDIN_HOST=linkedin-data-scraper.p.rapidapi.com

# Email Discovery
HUNTER_API_KEY=your-hunter-key

# OpenAI (optional, for enhanced personalization)
OPENAI_API_KEY=your-openai-key
```

---

## 📊 Cost Breakdown

### Free Tier Option (Best for starting):
- ✅ **Hunter.io**: 50 emails/month FREE
- ✅ **RapidAPI**: 100-500 requests/month FREE (varies by API)
- ✅ **Apify**: $5 free credit (~5,000 profiles)
- ✅ **Gmail SMTP**: Unlimited (500 emails/day limit)
- **Total**: **FREE** for ~100-500 leads/month

### Paid Tier (For scale):
- 💰 **Hunter.io**: $49/month (1,000 searches)
- 💰 **RapidAPI Instagram**: $10-30/month (10,000 requests)
- 💰 **RapidAPI LinkedIn**: $20-50/month (5,000 requests)
- 💰 **Apify**: $49/month (unlimited scraping)
- **Total**: ~$100-150/month for 10,000+ leads

---

## 🔧 Implementation Steps

### 1. Quick Start (No API Keys - Demo Mode)

The tool already works in **demo mode** without any API keys - it generates sample data for testing.

### 2. Email Only (Start Sending)

Just add:
```bash
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

You can manually import leads from CSV and use the tool for outreach!

### 3. Hunter.io (Email Discovery)

Add Hunter.io key to automatically find emails:
```bash
HUNTER_API_KEY=your-key
```

### 4. Instagram (via RapidAPI)

Add RapidAPI credentials for Instagram scraping:
```bash
RAPIDAPI_KEY=your-key
RAPIDAPI_INSTAGRAM_HOST=instagram-scraper-api2.p.rapidapi.com
```

### 5. LinkedIn (via RapidAPI)

Add LinkedIn scraping capability:
```bash
RAPIDAPI_LINKEDIN_HOST=linkedin-data-scraper.p.rapidapi.com
```

---

## 🚨 Legal & Compliance

### ⚠️ Important Warnings:

1. **Scraping Terms**: Instagram and LinkedIn prohibit automated scraping in their ToS
2. **Rate Limits**: Always respect API rate limits
3. **Personal Data**: EU GDPR and California CCPA apply
4. **CAN-SPAM**: Include unsubscribe in all emails

### ✅ Best Practices:

- Use official APIs when possible
- If scraping, use dedicated services (RapidAPI, Apify)
- Add delays between requests
- Never sell or share personal data
- Provide clear opt-out mechanism
- Only contact business emails for B2B

---

## 🎯 Recommended Setup for COLLIDE AI

**For fashion/beauty brand outreach:**

```bash
# Start with these (under $20/month):
✅ Hunter.io FREE tier (50 emails/month)
✅ RapidAPI Instagram Scraper ($10/month)
✅ Gmail (free)

# Add later for scale:
💰 RapidAPI LinkedIn ($30/month)
💰 Hunter.io Pro ($49/month)
💰 OpenAI API ($20/month for better messages)
```

---

## 📝 Next Steps

1. **Choose your integration level** (demo → email → scraping → full)
2. **Sign up for services** (start with Hunter.io FREE)
3. **Add API keys to .env**
4. **Update lead_gen.py** (I'll create updated version)
5. **Test with small campaigns** (10-20 leads)
6. **Scale gradually**

---

## 💡 Alternative: Manual Import

**Don't want to deal with APIs?**

You can also:
1. Manually search Instagram/LinkedIn
2. Export to CSV
3. Upload to the lead gen tool
4. Use for qualification and outreach

---

## 🆘 Need Help?

- **RapidAPI Hub**: Browse 1000+ APIs: https://rapidapi.com/hub
- **Apify Store**: Pre-built scrapers: https://apify.com/store
- **Hunter.io Docs**: https://hunter.io/api-documentation
- **Instagram Graph API**: https://developers.facebook.com/docs/instagram-api/

---

**Ready to connect real APIs?** Let me know which integration you want to set up first!

I can create:
1. Updated `lead_gen.py` with RapidAPI integration
2. Helper script to test API connections
3. CSV import feature for manual leads
4. Bulk email sending for imported lists

What would you like to tackle first? 🚀
