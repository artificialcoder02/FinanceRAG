import streamlit as st
import requests
from typing import Optional

def render_login_page(api_url: str = "http://localhost:8000"):
    """Render beautiful animated login/signup page"""
    
    # Custom CSS for animations
    st.markdown("""
    <style>
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Animated gradient background */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Inter', sans-serif;
        }
        
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        /* Login container */
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Title styling - WHITE with shadow */
        .login-title {
            font-family: 'Poppins', sans-serif;
            font-size: 4rem;
            font-weight: 800;
            color: white;
            text-align: center;
            margin-bottom: 0.5rem;
            text-shadow: 
                2px 2px 4px rgba(0, 0, 0, 0.3),
                0 0 20px rgba(255, 255, 255, 0.5),
                0 0 40px rgba(255, 255, 255, 0.3);
            letter-spacing: -1px;
            animation: fadeInDown 0.8s ease-out;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-subtitle {
            font-family: 'Inter', sans-serif;
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1rem;
            font-weight: 400;
            margin-bottom: 2.5rem;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
            letter-spacing: 0.5px;
            animation: fadeIn 1s ease-out 0.2s both;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            padding: 12px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            padding: 12px;
            font-weight: bold;
            transition: all 0.3s ease;
            background: linear-gradient(90deg, #1f77b4, #2ca02c);
            color: white;
            border: none;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and title
        st.markdown('<h1 class="login-title">💰 FinanceRAG</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Multi-Agent Financial Intelligence System</p>', unsafe_allow_html=True)
        
        # Tabs for Login/Signup
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="your@email.com")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    remember_me = st.checkbox("Remember me")
                with col_b:
                    st.markdown("[Forgot password?](#)")
                
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if submit:
                    if not email or not password:
                        st.error("⚠️ Please fill in all fields")
                    else:
                        with st.spinner("🔄 Logging in..."):
                            success, result = login_user(api_url, email, password)
                            
                            if success:
                                st.success("✅ Login successful!")
                                # Store in session state
                                st.session_state.access_token = result["access_token"]
                                st.session_state.user = result["user"]
                                st.session_state.authenticated = True
                                st.rerun()
                            else:
                                st.error(f"❌ {result}")
        
        with tab2:
            st.markdown("### Create Account")
            
            with st.form("signup_form"):
                full_name = st.text_input("👤 Full Name", placeholder="John Doe")
                username = st.text_input("🏷️ Username", placeholder="johndoe")
                email_signup = st.text_input("📧 Email", placeholder="your@email.com", key="signup_email")
                password_signup = st.text_input("🔒 Password", type="password", placeholder="Min 8 chars, 1 uppercase, 1 number", key="signup_password")
                password_confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Re-enter password")
                
                # Password strength indicator
                if password_signup:
                    strength = check_password_strength(password_signup)
                    if strength == "Strong":
                        st.success(f"✅ Password strength: {strength}")
                    elif strength == "Medium":
                        st.warning(f"⚠️ Password strength: {strength}")
                    else:
                        st.error(f"❌ Password strength: {strength}")
                
                agree_terms = st.checkbox("I agree to the Terms and Conditions")
                
                submit_signup = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if submit_signup:
                    if not all([full_name, username, email_signup, password_signup, password_confirm]):
                        st.error("⚠️ Please fill in all fields")
                    elif password_signup != password_confirm:
                        st.error("❌ Passwords do not match")
                    elif not agree_terms:
                        st.error("⚠️ Please agree to the terms and conditions")
                    else:
                        with st.spinner("🔄 Creating account..."):
                            success, result = register_user(api_url, email_signup, username, password_signup, full_name)
                            
                            if success:
                                st.success("✅ Account created successfully!")
                                st.info("📧 Please check your email to verify your account (simulated for now)")
                                st.balloons()
                                
                                # Auto-login after registration
                                with st.spinner("🔄 Logging you in..."):
                                    login_success, login_result = login_user(api_url, email_signup, password_signup)
                                    if login_success:
                                        st.session_state.access_token = login_result["access_token"]
                                        st.session_state.user = login_result["user"]
                                        st.session_state.authenticated = True
                                        st.rerun()
                            else:
                                st.error(f"❌ {result}")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: white; font-size: 0.9rem;'>"
            "🔒 Secure Authentication • 🇮🇳 India-First Context • 🤖 8 AI Agents"
            "</p>",
            unsafe_allow_html=True
        )

def login_user(api_url: str, email: str, password: str) -> tuple[bool, dict]:
    """Login user and get access token"""
    try:
        response = requests.post(
            f"{api_url}/auth/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            error_detail = response.json().get("detail", "Login failed")
            return False, error_detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Is the API running?"
    except Exception as e:
        return False, str(e)

def register_user(api_url: str, email: str, username: str, password: str, full_name: str) -> tuple[bool, dict]:
    """Register a new user"""
    try:
        response = requests.post(
            f"{api_url}/auth/register",
            json={
                "email": email,
                "username": username,
                "password": password,
                "full_name": full_name
            }
        )
        
        if response.status_code == 200:
            return True, response.json()
        else:
            error_detail = response.json().get("detail", "Registration failed")
            return False, error_detail
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to server. Is the API running?"
    except Exception as e:
        return False, str(e)

def check_password_strength(password: str) -> str:
    """Check password strength"""
    if len(password) < 8:
        return "Weak"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    strength_score = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength_score >= 3 and len(password) >= 10:
        return "Strong"
    elif strength_score >= 2:
        return "Medium"
    else:
        return "Weak"

def logout_user():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.access_token = None
    st.session_state.user = None
    st.rerun()
