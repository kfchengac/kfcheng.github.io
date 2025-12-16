# 📋 COLLIDE AI - Quick Reference Card

Print this or keep it handy while working on your platform!

---

## 🚀 START THE SERVER

```bash
cd ~/Documents/collide-ai-platform
PORT=8080 python3 app.py
```

**Access at:**
- Chat: http://localhost:8080
- Admin: http://localhost:8080/admin/login (admin / collide2025)
- Leads: http://localhost:8080/lead-gen

---

## 📁 KEY FILES TO CUSTOMIZE

| File | What It Controls | Priority |
|------|------------------|----------|
| `templates/index.html` | Customer chat interface text | **HIGH** |
| `app.py` (lines 60-150) | AI knowledge & responses | **HIGH** |
| `lead_gen.py` (lines 180-250) | Lead scoring criteria | **MEDIUM** |
| `lead_gen.py` (lines 300-350) | Outreach email template | **HIGH** |
| `.env` | API keys & passwords | **HIGH** |
| `static/style.css` | Colors & styling | **LOW** |

---

## 🔑 REQUIRED IN .ENV FILE

```bash
# Minimum to start:
EMAIL_USER=your@gmail.com
EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx  # App Password!

# Optional but recommended:
OPENAI_API_KEY=sk-xxxxx              # Better AI ($5-10/mo)
HUNTER_API_KEY=xxxxx                 # Find emails (FREE tier)
RAPIDAPI_KEY=xxxxx                   # Real leads ($10/mo)
```

---

## 🎯 CUSTOMIZATION CHECKLIST

### Must Do (30 minutes):
- [ ] Change admin password (app.py line 200)
- [ ] Update hero text (templates/index.html line 20)
- [ ] Add your services list (templates/index.html line 50)
- [ ] Edit starter prompts (templates/index.html line 100)
- [ ] Set up Gmail App Password (.env file)

### Should Do (2 hours):
- [ ] Customize AI knowledge base (app.py lines 60-150)
- [ ] Personalize outreach template (lead_gen.py line 300)
- [ ] Adjust lead scoring (lead_gen.py line 200)
- [ ] Add your pricing (app.py knowledge base)
- [ ] Update target hashtags/keywords (lead_gen.py line 400)

### Nice to Have (4 hours):
- [ ] Add OpenAI API key for smarter responses
- [ ] Sign up for Hunter.io (free tier)
- [ ] Create custom color scheme (static/style.css)
- [ ] Write case studies in knowledge base
- [ ] Set up RapidAPI for real leads

---

## 💰 COST TIERS

| Tier | Monthly Cost | Capacity | Best For |
|------|--------------|----------|----------|
| **Free** | $0 | Demo mode | Testing |
| **Starter** | $10-25 | 100-200 leads | First 6 months |
| **Growth** | $50-100 | 1,000-5,000 leads | Established business |
| **Scale** | $200-500 | 10,000+ leads | Agency/Team |

---

## 🔧 COMMON TERMINAL COMMANDS

```bash
# Start server
cd ~/Documents/collide-ai-platform && PORT=8080 python3 app.py

# Stop server
Ctrl+C  (or: lsof -ti:8080 | xargs kill -9)

# Edit .env file
nano .env

# Edit main app
nano app.py

# Test lead generation
python3 lead_gen.py

# Interactive API setup
python3 setup_apis.py

# View logs
tail -f app.log  (if you set up logging)
```

---

## 🎨 WHERE TO CHANGE SPECIFIC THINGS

### Change Business Name:
- `templates/index.html` line 17: `<h1>COLLIDE AI</h1>`
- `templates/admin_dashboard.html` line 15
- `app.py` line 50: `print("🎨 COLLIDE AI Platform Starting...")`

### Change Services List:
- `templates/index.html` lines 45-60

### Change Pricing Display:
- `templates/index.html` lines 75-85
- `app.py` knowledge_base → 'pricing' section

### Change Default Hashtags:
- `lead_gen.py` line 410: `default_instagram_hashtags = [...]`

### Change Qualification Score:
- `lead_gen.py` line 245: `lead['qualified'] = score >= 50`

### Change Email Subject Line:
- `lead_gen.py` line 310: `subject = f"Elevate {company}'s brand strategy"`

---

## 📧 GMAIL APP PASSWORD SETUP

1. **Enable 2FA**: https://myaccount.google.com/security
2. **Generate password**: https://myaccount.google.com/apppasswords
3. **Copy 16-char code** (looks like: xxxx xxxx xxxx xxxx)
4. **Add to .env**: `EMAIL_PASSWORD=xxxxxxxxxxxxxxxx` (no spaces!)

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Can't access localhost:8080 | Server not running → Start it |
| Email won't send | Need App Password, not regular password |
| No leads found | Add RapidAPI key or use demo mode |
| 500 Error | Check terminal for Python error |
| Chat not responding | Check browser console (F12) |
| Changes not showing | Hard refresh: Ctrl+Shift+R |

---

## 📚 DOCUMENTATION GUIDE

| Need to... | Read this file... |
|------------|-------------------|
| Understand everything | **MASTER_README.md** ⭐ |
| Set up APIs | API_SETUP_GUIDE.md |
| Quick lead gen guide | LEAD_GEN_QUICKSTART.md |
| Technical details | LEAD_GEN_README.md |
| Setup checklist | INSTALLATION_COMPLETE.md |

---

## 🎯 FIRST WEEK GOALS

### Day 1: Customize Text
- Change all "COLLIDE" references to your brand
- Update services list
- Edit welcome message

### Day 2: Set Up Email
- Get Gmail App Password
- Add to .env
- Send test email to yourself

### Day 3: Customize AI
- Update knowledge base with your expertise
- Add your frameworks
- Test conversations

### Day 4: Personalize Outreach
- Rewrite email template in your voice
- Adjust lead scoring criteria
- Add your target hashtags

### Day 5: Test Everything
- Run demo lead campaign
- Test email sending
- Try all 4 AI personas
- Check admin dashboard

### Day 6-7: First Real Campaign (Optional)
- Add Hunter.io free account
- Run campaign with 20 leads
- Track responses

---

## 🆘 EMERGENCY COMMANDS

```bash
# Server won't stop?
lsof -ti:8080 | xargs kill -9

# Broke something? Restore backup:
cp app.py.backup.YYYYMMDD_HHMMSS app.py

# Reset .env?
cp .env.example .env

# Start fresh terminal:
source ~/.zshrc

# Check if server is running:
lsof -i :8080
```

---

## ✅ VERIFICATION CHECKLIST

Before launching to real clients:

- [ ] Server starts without errors
- [ ] Chat interface loads and responds
- [ ] Admin login works (changed default password!)
- [ ] Lead gen tool loads
- [ ] Can send test email successfully
- [ ] All text says YOUR business name
- [ ] Services list matches what you offer
- [ ] Pricing is accurate
- [ ] AI responses sound like you
- [ ] Outreach email sounds professional

---

## 🎉 LAUNCH CHECKLIST

When ready to go live:

- [ ] Change admin password (security!)
- [ ] Add custom domain
- [ ] Deploy to Railway/Render
- [ ] Set up SSL certificate (automatic on Railway)
- [ ] Test on mobile devices
- [ ] Share link with 5 test users
- [ ] Monitor for errors
- [ ] Check email deliverability
- [ ] Set up analytics (Google Analytics)
- [ ] Create backup schedule

---

**Keep this card handy! Pin it to your desktop or print it out. 📌**

Need more detail? Open **MASTER_README.md**
