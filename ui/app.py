import streamlit as st
import requests
import json
from datetime import datetime
import time
import os
from auth_ui import render_login_page, logout_user

# Page configuration
st.set_page_config(
    page_title="FinanceRAG - Financial Intelligence",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0
if 'avg_response_time' not in st.session_state:
    st.session_state.avg_response_time = 0
if 'response_times' not in st.session_state:
    st.session_state.response_times = []

# API URL - use environment variable for deployment, default to localhost
API_URL = os.getenv("API_URL", st.secrets.get("API_URL", "http://localhost:8000"))

# Check authentication
if not st.session_state.authenticated:
    render_login_page(API_URL)
    st.stop()

# User is authenticated - show main app
# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .example-query {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        cursor: pointer;
    }
    .stat-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .source-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
    }
    .user-badge {
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">💰 FinanceRAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-Agent Financial Intelligence System | India-First Context</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # User info
    user = st.session_state.user
    st.markdown(f"""
    <div class="user-badge">
        👤 {user['full_name']}
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"@{user['username']} • {user['role'].title()}")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout_user()
    
    st.markdown("---")
    
    st.header("⚙️ Configuration")
    
    # Display Options
    with st.expander("🎛️ Display Options", expanded=False):
        show_sources = st.checkbox("Show Sources", value=True)
        show_evaluation = st.checkbox("Show Evaluation", value=True)
        show_metadata = st.checkbox("Show Metadata", value=False)
        max_sources = st.slider("Max Sources to Display", 1, 20, 5)
    
    # Statistics
    st.header("📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", user.get('total_queries', 0))
    with col2:
        avg_time = st.session_state.avg_response_time
        st.metric("Avg Response", f"{avg_time:.1f}s" if avg_time > 0 else "N/A")
    
    # Chat History
    st.header("📜 Chat History")
    if st.button("🗑️ Clear History"):
        st.session_state.chat_history = []
        st.session_state.total_queries = 0
        st.session_state.response_times = []
        st.session_state.avg_response_time = 0
        st.rerun()
    
    if st.session_state.chat_history:
        for idx, item in enumerate(reversed(st.session_state.chat_history[-10:])):
            with st.expander(f"Q{len(st.session_state.chat_history) - idx}: {item['query'][:40]}..."):
                st.write(f"**Time:** {item['timestamp']}")
                st.write(f"**Score:** {item.get('score', 'N/A')}")
                if st.button(f"Reuse Query", key=f"reuse_{idx}"):
                    st.session_state.reuse_query = item['query']
                    st.rerun()
    else:
        st.info("No queries yet")
    
    # Admin Panel Link
    if user.get('role') == 'admin':
        st.markdown("---")
        if st.button("👑 Admin Panel", use_container_width=True):
            st.session_state.show_admin = True
            st.rerun()
    
    # Info
    st.markdown("---")
    st.info("💡 **Tip:** Use example queries below to get started!")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Example Queries Section
    st.subheader("💡 Example Queries")
    
    example_queries = {
        "🏦 Banking": [
            "What is the current RBI repo rate?",
            "Explain the difference between NEFT and RTGS",
            "What are the latest RBI guidelines on digital lending?"
        ],
        "📈 Markets": [
            "What is SEBI's role in the stock market?",
            "Explain the concept of mutual funds in India",
            "What are the latest changes in IPO regulations?"
        ],
        "💳 Taxation": [
            "What is GST and how does it work in India?",
            "Explain the income tax slabs for FY 2024-25",
            "What are the tax benefits of investing in ELSS?"
        ],
        "🏢 Corporate": [
            "What is the Companies Act 2013?",
            "Explain the concept of NBFC in India",
            "What are the latest SEBI regulations for listed companies?"
        ]
    }
    
    selected_category = st.selectbox("Select Category", list(example_queries.keys()))
    
    cols = st.columns(len(example_queries[selected_category]))
    for idx, example in enumerate(example_queries[selected_category]):
        with cols[idx]:
            if st.button(example, key=f"example_{selected_category}_{idx}", use_container_width=True):
                st.session_state.selected_query = example
                st.rerun()

with col2:
    # Quick Stats
    st.subheader("📊 Quick Stats")
    st.markdown(f"""
    <div class="stat-box">
        <h4>🤖 Active Agents: 8</h4>
        <p>Web Search • Scraper • Preprocessing<br>
        Indexing • Retrieval • Reranker<br>
        Answering • Evaluation</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Query Input
query_input = st.text_area(
    "🔍 Ask your financial question:",
    value=st.session_state.get('selected_query', st.session_state.get('reuse_query', '')),
    placeholder="e.g., What is the current RBI repo rate? How does GST work in India?",
    height=100,
    key="query_input"
)

# Clear selected query after using it
if 'selected_query' in st.session_state:
    del st.session_state.selected_query
if 'reuse_query' in st.session_state:
    del st.session_state.reuse_query

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    ask_button = st.button("🚀 Ask FinanceRAG", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🔄 Clear", use_container_width=True)
with col3:
    if st.session_state.chat_history:
        export_button = st.button("💾 Export", use_container_width=True)
    else:
        export_button = False

if clear_button:
    st.rerun()

# Export functionality
if export_button:
    export_data = {
        "user": user['email'],
        "total_queries": st.session_state.total_queries,
        "avg_response_time": st.session_state.avg_response_time,
        "chat_history": st.session_state.chat_history
    }
    st.download_button(
        label="📥 Download Chat History (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name=f"financerag_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# Process query
if ask_button:
    if not query_input or query_input.strip() == "":
        st.warning("⚠️ Please enter a query.")
    else:
        start_time = time.time()
        
        # Progress indicator
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        stages = [
            "🔍 Searching the web...",
            "🌐 Scraping content...",
            "✂️ Processing text...",
            "📊 Indexing documents...",
            "🔎 Retrieving relevant info...",
            "🎯 Reranking results...",
            "💬 Generating answer...",
            "✅ Evaluating response..."
        ]
        
        for idx, stage in enumerate(stages):
            progress_text.text(stage)
            progress_bar.progress((idx + 1) / len(stages))
            time.sleep(0.1)
        
        try:
            # Make authenticated request
            headers = {
                "Authorization": f"Bearer {st.session_state.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{API_URL}/ask",
                json={"query": query_input},
                headers=headers,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Update statistics
            st.session_state.total_queries += 1
            st.session_state.response_times.append(response_time)
            st.session_state.avg_response_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "query": query_input,
                "answer": data["answer"],
                "sources": data["sources"],
                "evaluation": data["evaluation"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response_time": response_time,
                "score": data["evaluation"].get("score", "N/A")
            })
            
            # Clear progress indicators
            progress_text.empty()
            progress_bar.empty()
            
            # Display results
            st.success(f"✅ Answer generated in {response_time:.2f} seconds!")
            
            # Answer section
            st.markdown("### 📝 Answer")
            st.markdown(data["answer"])
            
            # Metadata
            if show_metadata:
                with st.expander("🔍 Query Metadata"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Response Time", f"{response_time:.2f}s")
                    with col2:
                        st.metric("Sources Found", len(data["sources"]))
                    with col3:
                        st.metric("Quality Score", data["evaluation"].get("score", "N/A"))
            
            # Evaluation
            if show_evaluation:
                with st.expander("📊 Evaluation Metrics", expanded=False):
                    eval_data = data["evaluation"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Quality Score", eval_data.get("score", "N/A"))
                    with col2:
                        feedback_count = len(eval_data.get("feedback", []))
                        st.metric("Feedback Items", feedback_count)
                    
                    if eval_data.get("feedback"):
                        st.write("**Feedback:**")
                        for item in eval_data["feedback"]:
                            st.write(f"- {item}")
                    else:
                        st.success("✅ No issues found!")
            
            # Sources
            if show_sources and data["sources"]:
                st.markdown("### 📚 Sources")
                sources_to_show = data["sources"][:max_sources]
                
                for idx, source in enumerate(sources_to_show):
                    with st.container():
                        st.markdown(f"""
                        <div class="source-card">
                            <h4>📄 {idx+1}. {source.get('title', 'Unknown Title')}</h4>
                            <p><a href="{source.get('source', '#')}" target="_blank">{source.get('source', 'Unknown URL')}</a></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if len(data["sources"]) > max_sources:
                    st.info(f"ℹ️ Showing {max_sources} of {len(data['sources'])} sources. Adjust in sidebar to see more.")
            
            # Action buttons for result
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👍 Helpful"):
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("👎 Not Helpful"):
                    st.info("We'll improve our responses!")
            with col3:
                if st.button("📋 Copy Answer"):
                    st.code(data["answer"], language=None)
                    st.info("Answer displayed above for copying")
            
        except requests.exceptions.HTTPError as e:
            progress_text.empty()
            progress_bar.empty()
            if e.response.status_code == 401:
                st.error("❌ Session expired. Please login again.")
                logout_user()
            else:
                st.error(f"❌ Server error: {e}")
        except requests.exceptions.ConnectionError:
            progress_text.empty()
            progress_bar.empty()
            st.error("❌ Could not connect to the backend API. Is it running?")
            st.info("💡 Start the API with: `uvicorn api.main:app --reload`")
        except requests.exceptions.Timeout:
            progress_text.empty()
            progress_bar.empty()
            st.error("⏱️ Request timed out. The query might be too complex.")
        except Exception as e:
            progress_text.empty()
            progress_bar.empty()
            st.error(f"❌ An error occurred: {e}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🔗 [Documentation](../DOCUMENTATION.md)")
with col2:
    st.markdown("🐛 [Report Issue](https://github.com)")
with col3:
    st.markdown("⭐ [Star on GitHub](https://github.com)")
