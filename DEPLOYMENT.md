# 🚀 Quick Deployment Guide

## Free Deployment in 3 Steps

### 1. MongoDB Atlas (Database)
1. Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create **M0 FREE** cluster
3. Add database user
4. Allow access from anywhere (0.0.0.0/0)
5. Get connection string

### 2. Render (API Backend)
1. Push code to GitHub
2. Sign up at [render.com](https://render.com)
3. New Web Service → Connect GitHub repo
4. Add environment variables:
   - `MONGODB_URL`: Your Atlas connection string
   - `GOOGLE_API_KEY`: Your Google API key
   - `ADMIN_PASSWORD`: Strong password
5. Deploy!

### 3. Streamlit Cloud (Frontend)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. New app → Select your repo
3. Main file: `ui/app.py`
4. Add secret: `API_URL = "https://your-api.onrender.com"`
5. Deploy!

## Your App is Live! 🎉

**See full deployment guide in [walkthrough.md](file:///C:/Users/rctuh/.gemini/antigravity/brain/6e31e596-63ca-4348-846c-fb46050d1e10/walkthrough.md)**

---

## Cost: $0/month

- MongoDB Atlas Free: 512MB
- Render Free: 750 hours/month
- Streamlit Cloud: Unlimited public apps

---

## Files Created for Deployment

- ✅ `render.yaml` - Render configuration
- ✅ `runtime.txt` - Python version
- ✅ `.streamlit/config.toml` - Streamlit config
- ✅ Updated `ui/app.py` - Dynamic API URL
