import streamlit as st
from streamlit_chat import message
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="ByteBuddy - AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'hf_token' not in st.session_state:
    st.session_state.hf_token = os.getenv("HF_TOKEN", "")

# Sidebar configuration
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Hugging Face Token input
    hf_token_input = st.text_input(
        "Enter your Hugging Face Token",
        value=st.session_state.hf_token,
        type="password",
        help="Get your token from https://huggingface.co/settings/tokens"
    )
    
    if hf_token_input:
        st.session_state.hf_token = hf_token_input
    
    # Model selection
    model = st.selectbox(
        "Select AI Model",
        [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "meta-llama/Llama-2-7b-chat-hf",
            "HuggingFaceH4/zephyr-7b-beta",
            "tiiuae/falcon-7b-instruct"
        ],
        help="Choose the AI model to use for responses"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.1,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random/creative"
    )
    
    # Max tokens slider
    max_tokens = st.slider(
        "Max Response Length",
        min_value=50,
        max_value=1024,
        value=256,
        step=50,
        help="Maximum number of tokens in response"
    )
    
    # Top P slider
    top_p = st.slider(
        "Top P (Diversity)",
        min_value=0.0,
        max_value=1.0,
        value=0.95,
        step=0.05,
        help="Controls diversity via nucleus sampling"
    )
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Display chat info
    st.info(f"📊 Messages in chat: {len(st.session_state.messages)}")

# Main chat interface
st.title("🤖 ByteBuddy - AI Chatbot")
st.markdown("*Your intelligent conversation partner powered by Hugging Face*")

# Display chat messages
for idx, msg in enumerate(st.session_state.messages):
    if msg['role'] == 'user':
        st.chat_message("user").write(msg['content'])
    else:
        st.chat_message("assistant").write(msg['content'])

# Chat input
user_input = st.chat_input(
    "Type your message here...",
    placeholder="Ask me anything!",
    disabled=not st.session_state.hf_token
)

if user_input:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.chat_message("user").write(user_input)
    
    # Generate AI response
    try:
        with st.spinner("🤔 Thinking..."):
            # Initialize Hugging Face client
            client = InferenceClient(
                model=model,
                token=st.session_state.hf_token
            )
            
            # Create prompt from conversation history
            prompt = ""
            for msg in st.session_state.messages[:-1]:  # Exclude current user message for context
                role = "User" if msg['role'] == 'user' else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
            prompt += f"User: {user_input}\nAssistant:"
            
            # Generate response
            response = client.text_generation(
                prompt=prompt,
                temperature=temperature,
                max_new_tokens=max_tokens,
                top_p=top_p,
            )
        
        assistant_message = response.strip()
        
        # Add assistant message to session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        
        # Display assistant message
        st.chat_message("assistant").write(assistant_message)
        
    except Exception as e:
        error_message = str(e)
        if "401" in error_message or "Unauthorized" in error_message:
            st.error("❌ Authentication Error: Invalid Hugging Face token. Please check your token.")
        elif "429" in error_message:
            st.error("⚠️ Rate Limited: Too many requests. Please wait a moment and try again.")
        elif "model not found" in error_message.lower():
            st.error(f"❌ Model Error: The selected model is not available. Please choose a different model.")
        else:
            st.error(f"❌ An error occurred: {error_message}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; font-size: 12px;">
    <p>ByteBuddy v1.0 | Powered by Hugging Face Inference API</p>
    <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
