"""
Configuration file for ByteBuddy application
"""

# Streamlit page configuration
PAGE_CONFIG = {
    "page_title": "ByteBuddy - AI Chatbot",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Available models from Hugging Face
AVAILABLE_MODELS = [
    "mistralai/Mistral-7B-Instruct-v0.2",
    "meta-llama/Llama-2-7b-chat-hf",
    "HuggingFaceH4/zephyr-7b-beta",
    "tiiuae/falcon-7b-instruct"
]

# Model descriptions
MODEL_DESCRIPTIONS = {
    "mistralai/Mistral-7B-Instruct-v0.2": "🚀 Fast and efficient - Recommended for quick responses",
    "meta-llama/Llama-2-7b-chat-hf": "💬 Great for conversations - Meta's Llama 2",
    "HuggingFaceH4/zephyr-7b-beta": "⚡ Balanced performance - Based on Mistral",
    "tiiuae/falcon-7b-instruct": "🦅 High performance - TII's powerful model"
}

# Default settings
DEFAULT_SETTINGS = {
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "temperature": 0.7,
    "max_tokens": 256,
    "top_p": 0.95,
}

# Temperature presets
TEMPERATURE_PRESETS = {
    "Focused": 0.3,
    "Balanced": 0.7,
    "Creative": 1.5,
}

# API configuration
API_TIMEOUT = 60  # seconds
MAX_RETRIES = 3

# UI Configuration
CHAT_HEIGHT = 400  # pixels
MESSAGE_BOX_HEIGHT = 100  # pixels

# Colors
COLORS = {
    "primary": "#0066cc",
    "secondary": "#f0f2f6",
    "success": "#09ab3b",
    "error": "#ff0000",
    "warning": "#ff8c00",
}

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 10
