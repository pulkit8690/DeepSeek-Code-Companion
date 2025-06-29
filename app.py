import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Custom CSS styling for a modern look
st.markdown("""
<style>
    /* Global style */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Background with gradient */
    .main {
        background: linear-gradient(135deg, #1d1f21, #3b3e46);
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #2a2d33;
        border-right: 2px solid #444;
    }
    
    /* Title and caption styling */
    .css-18e3th9 {  /* Adjust container class if necessary */
        text-align: center;
    }
    
    /* Input styling */
    .stTextInput textarea {
        color: #ffffff !important;
        background-color: #3b3e46 !important;
        border: 1px solid #555 !important;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        color: #ffffff !important;
        background-color: #3b3e46 !important;
        border: 1px solid #555 !important;
        transition: background-color 0.3s ease;
    }
    .stSelectbox div[data-baseweb="select"]:hover {
        background-color: #505359 !important;
    }
    .stSelectbox svg {
        fill: #ffffff !important;
    }
    .stSelectbox option {
        background-color: #2a2d33 !important;
        color: #ffffff !important;
    }
    div[role="listbox"] div {
        background-color: #2a2d33 !important;
        color: #ffffff !important;
    }
    
    /* Chat message styling */
    .chat-message {
        background: #2d2f33;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .chat-message.ai {
        border-left: 4px solid #4caf50;
    }
    
    .chat-message.user {
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Page Title and Caption
st.title("🧠 DeepSeek Code Companion")
st.caption("🚀 Your AI Pair Programmer with Debugging Superpowers")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    selected_model = st.selectbox(
        "Choose Model",
        ["deepseek-r1:1.5b", "deepseek-r1:3b"],
        index=0
    )
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🐍 Python Expert  
    - 🐞 Debugging Assistant  
    - 📝 Code Documentation  
    - 💡 Solution Design  
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# Initialize the chat engine
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.3
)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solutions "
    "with strategic print statements for debugging. Always respond in English."
)

# Session state management for message log
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? 💻"}]

# Chat container
chat_container = st.container()

# Display chat messages with enhanced styling
with chat_container:
    for message in st.session_state.message_log:
        role = message["role"]
        custom_class = "ai" if role == "ai" else "user"
        with st.chat_message(role):
            st.markdown(f'<div class="chat-message {custom_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input and processing
user_query = st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain):
    processing_pipeline = prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()
