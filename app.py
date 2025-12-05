import streamlit as st
import os
import tempfile
import zipfile
from git import Repo
from dotenv import load_dotenv

# Import functions
from ingect_data import create_index_from_repo
from chat_engine import setup_query_engine, get_response

# Load environment variables
load_dotenv()

# Get the key specifically for Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

st.set_page_config(page_title="Dynamic Codebase Assistant (RAG)", layout="wide")

st.title("🤖 Codebase Assistant (Gemini RAG)")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file. Please add it.")
    st.stop()

# --- Initialization ---
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_ready" not in st.session_state:
    st.session_state.repo_ready = False

# --- Sidebar ---
with st.sidebar:
    st.header("Upload/Load Codebase")
    github_url = st.text_input("Enter GitHub Repository URL:", key="github_url")
    uploaded_file = st.file_uploader("Upload Codebase (ZIP file):", type=["zip"], key="zip_upload")
    code_language = st.selectbox("Select Code Language:", options=["python", "javascript", "java", "cpp", "markdown"], index=0)
    
    load_button = st.button("Load and Index Codebase", type="primary")

    if load_button:
        st.session_state.repo_ready = False
        st.session_state.query_engine = None
        st.session_state.messages = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = None
            
            # 1. Clone or Extract
            if github_url:
                with st.spinner(f"Cloning {github_url}..."):
                    try:
                        Repo.clone_from(github_url, tmpdir, depth=1)
                        repo_path = tmpdir
                    except Exception as e:
                        st.error(f"Error cloning repository: {e}")
                        st.stop()
            elif uploaded_file:
                with st.spinner("Extracting ZIP file..."):
                    try:
                        with zipfile.ZipFile(uploaded_file, 'r') as z:
                            z.extractall(tmpdir)
                        repo_path = tmpdir
                    except Exception as e:
                        st.error(f"Error extracting ZIP file: {e}")
                        st.stop()
            else:
                st.warning("Please provide a GitHub URL or upload a ZIP file.")
                st.stop()

            # 2. Create Index
            if repo_path:
                with st.spinner("Processing Codebase..."):
                    try:
                        # PASS KEY HERE
                        index = create_index_from_repo(repo_path, code_language, api_key=GOOGLE_API_KEY)
                        
                        # PASS KEY HERE TOO
                        st.session_state.query_engine = setup_query_engine(index, api_key=GOOGLE_API_KEY)
                        
                        st.session_state.repo_ready = True
                        st.success(f"Codebase indexed! Start chatting.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.stop()

# --- Chat Interface ---
if not st.session_state.repo_ready:
    st.info("💡 Please load a codebase using the sidebar to begin.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the code..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = get_response(st.session_state.query_engine, prompt)
                    
                    full_response = str(response)
                    source_info = "\n\n**Sources:**\n"
                    for node in response.source_nodes:
                        file_path = node.metadata.get('file_path', 'N/A')
                        source_info += f"- `{file_path}`\n"
                    
                    final_output = full_response + source_info
                    st.markdown(final_output)
                    st.session_state.messages.append({"role": "assistant", "content": final_output})
                except Exception as e:
                    st.error(f"Error generating response: {e}")