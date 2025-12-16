# 🎨 COLLIDE AI Platform

A complete web platform for brand consulting with AI-powered advisor and staff backend management.

## Features

### Customer Interface 💬
- **Interactive Chat**: Real-time conversation with COLLIDE AI brand advisor
- **Smart Responses**: AI-powered or rule-based consultation on:
  - Brand strategy & positioning
  - Visual identity development
  - Target audience definition
  - Business development & pricing
  - Competitive differentiation
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Session Management**: Continuous conversations with context

### Admin Dashboard 🔧
- **AI Model Control**: 
  - Toggle between OpenAI API and rule-based responses
  - Configure API keys and model selection (GPT-4, GPT-3.5)
  - Adjust temperature and token limits
- **Conversation Analytics**:
  - View all customer conversations
  - Export conversation data as JSON
  - Track session metrics
- **Real-time Monitoring**: System status and usage statistics

## Installation

### Streamlit Demo (GitHub/Streamlit Cloud)
1. Python version: 3.13.9 (see `runtime.txt`).
2. Install deps (uv or pip):
   ```bash
   uv pip install -r requirements.txt
   # or: pip install -r requirements.txt
   ```
3. Run locally:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Deploy on Streamlit Cloud: push to GitHub with this `requirements.txt`; set secrets if needed (no secrets required for the demo).

### Netlify (Flask via Functions)
1. Ensure Netlify has a Python runtime (3.11+; if 3.13 is unavailable, pin 3.11 in Netlify env var `PYTHON_VERSION`).
2. Netlify reads `requirements.txt` and builds functions in `netlify/functions/` with [netlify.toml](netlify.toml).
3. Build command (configured): `bash scripts/netlify_build_debug.sh` installs deps and copies `static/` to `public/static/` for publishing.
4. Publish dir: `public`; Functions dir: `netlify/functions`.
5. If you add secrets (e.g., `OPENAI_API_KEY`), set them in Netlify Site settings → Environment variables.

### 1. Clone or Download

Save all files in a project folder (for example `~/Documents/collide-ai-platform/`):

```
collide-ai-platform/
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── admin_login.html
│   └── admin_dashboard.html
└── static/
    ├── style.css
    ├── admin.css
    ├── script.js
    └── admin.js
```

### 2. Install Dependencies

```bash
cd ~/Documents/collide-ai-platform
pip3 install -r requirements.txt
```

### 3. (Optional) Set Environment Variables

```bash
# For OpenAI API integration
export OPENAI_API_KEY='your-api-key-here'

# For session security (recommended for production)
export SECRET_KEY='your-secret-key-here'
```

### 4. Run the Application

```bash
# Default PORT is 5001 if not set; you can override it
PORT=5001 PUBLIC_URL=http://localhost:5001 python3 app.py
```

The server will start at (by default):
- **Customer Interface**: http://localhost:5001
- **Admin Dashboard**: http://localhost:5001/admin/login

If you see "Address already in use", try a different port:

```bash
PORT=5002 PUBLIC_URL=http://localhost:5002 python3 app.py
```

## Usage

### Customer Side

1. Visit http://localhost:5000
2. Start chatting with COLLIDE AI
3. Ask questions about:
   - Brand development
   - Visual identity
   - Business strategy
   - Target audience
   - And more!

### Admin Side

1. Visit http://localhost:5000/admin/login
2. Login credentials:
   - **Username**: `admin`
   - **Password**: `collide2025`
3. Access features:
   - **Settings**: Configure AI model and parameters
   - **Conversations**: View and export customer interactions
   - **Analytics**: Monitor usage statistics

## Configuration

### AI Mode Options

**Rule-Based Mode** (Default)
- No API key required
- Uses pre-defined strategic frameworks
- Instant responses
- Perfect for testing

**OpenAI API Mode**
- Requires OpenAI API key
- Dynamic, personalized responses
- Advanced conversational abilities
- Set in Admin Dashboard → Settings

### Model Parameters

Adjust in Admin Dashboard:
- **Model**: GPT-4 (more capable) or GPT-3.5 Turbo (faster/cheaper)
- **Temperature**: 0.0 (focused) to 1.0 (creative)
- **Max Tokens**: Response length limit (100-2000)

## Production Deployment

### Security Recommendations

1. **Change Admin Password**
   - Edit `ADMIN_CREDENTIALS` in `app.py`
   - Or use database with hashed passwords

2. **Set Secret Key**
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

3. **Use HTTPS**
   - Deploy behind reverse proxy (nginx)
   - Enable SSL/TLS certificates

4. **Database Integration**
   - Replace in-memory storage with PostgreSQL/MongoDB
   - Store conversations and settings persistently

### Deployment Options

**Heroku**
```bash
heroku create collide-ai-platform
git push heroku main
heroku config:set OPENAI_API_KEY=your-key
```

**Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**VPS (Ubuntu)**
```bash
sudo apt install python3-pip nginx
pip3 install -r requirements.txt
# Configure nginx as reverse proxy
# Set up systemd service
```

## API Endpoints

### Public Endpoints
- `POST /api/chat` - Send message, get AI response

### Admin Endpoints (Auth Required)
- `GET /admin/dashboard` - Dashboard view
- `GET/POST /admin/api/settings` - Get/update settings
- `GET /admin/api/conversations` - List conversations
- `GET /admin/api/conversations/export` - Export as JSON
- `POST /admin/api/conversations/clear` - Clear all

## Customization

### Brand Identity
Edit in `templates/index.html`:
- Logo and tagline
- Industry tags
- Welcome message
- Footer content

### AI Personality
Edit `SYSTEM_PROMPT` in `app.py`:
- Consulting style
- Areas of expertise
- Response tone

### Visual Design
Edit CSS files in `static/`:
- `style.css` - Customer interface
- `admin.css` - Admin dashboard
- Modify color scheme in `:root` variables

## Support

For issues or questions:
1. Check conversation logs in Admin Dashboard
2. Review browser console for JavaScript errors
3. Check Flask terminal output for backend errors

## License

Proprietary - COLLIDE AI Platform

---

Built with ❤️ for creative entrepreneurs in Fashion, Beauty, Lifestyle, and Design
