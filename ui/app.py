import streamlit as st
import requests
import json

st.set_page_config(page_title="FinanceRAG", page_icon="💰", layout="wide")

st.title("💰 FinanceRAG")
st.markdown("### Multi-Agent Financial Intelligence System")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", "http://localhost:8000/ask")
    st.info("Ensure the FastAPI backend is running: `uvicorn api.main:app --reload`")

# Main chat interface
query = st.text_input("Ask a financial question:", placeholder="e.g., What is the current RBI repo rate?")

if st.button("Ask FinanceRAG", type="primary"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Agents are working... (Searching -> Scraping -> Indexing -> Retrieving -> Answering)"):
            try:
                response = requests.post(api_url, json={"query": query})
                response.raise_for_status()
                data = response.json()
                
                # Display Answer
                st.markdown("### 📝 Answer")
                st.markdown(data["answer"])
                
                # Display Evaluation
                with st.expander("📊 Evaluation Metrics"):
                    st.json(data["evaluation"])
                
                # Display Sources
                st.markdown("### 📚 Sources")
                for idx, source in enumerate(data["sources"]):
                    with st.container():
                        st.markdown(f"**{idx+1}. {source.get('title', 'Unknown Title')}**")
                        st.markdown(f"*{source.get('source', 'Unknown URL')}*")
                        st.divider()
                        
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend API. Is it running?")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("Built with LangChain, ChromaDB, Ollama, and Streamlit")
