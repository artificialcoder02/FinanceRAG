# 🚀 Quick Start Guide - FinanceRAG with Authentication

## Prerequisites
- ✅ MongoDB running on `localhost:27017`
- ✅ Virtual environment activated
- ✅ Dependencies installed

## Start the App (2 Terminals)

### Terminal 1: API Server
```bash
cd c:\Users\rctuh\Desktop\VNIT\FinanceRAG
venv\Scripts\activate
uvicorn api.main:app --reload
```

**Wait for:** `✅ Admin user created: admin@financerag.com`

### Terminal 2: Streamlit UI
```bash
cd c:\Users\rctuh\Desktop\VNIT\FinanceRAG
venv\Scripts\activate
streamlit run ui/app.py
```

## Login

1. Open: **http://localhost:8501**
2. You'll see the animated login page
3. Login with:
   - **Email:** `admin@financerag.com`
   - **Password:** `Admin@123`
4. Click **🚀 Login**

## Done! 🎉

You're now logged in and can:
- Ask financial questions
- View your query history
- See your profile in the sidebar
- Logout anytime

---

## Create New Users

Click the **📝 Sign Up** tab and register:
- Full Name
- Username
- Email
- Password (min 8 chars, 1 uppercase, 1 number)

---

## Troubleshooting

**Can't connect to API?**
- Make sure MongoDB is running
- Check `.env` has `MONGODB_URL=mongodb://localhost:27017/`

**Session expired?**
- Logout and login again
- Tokens last 24 hours

---

For detailed documentation, see [walkthrough.md](file:///C:/Users/rctuh/.gemini/antigravity/brain/6e31e596-63ca-4348-846c-fb46050d1e10/walkthrough.md)
