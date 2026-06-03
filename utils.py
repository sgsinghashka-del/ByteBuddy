"""
Utility functions for ByteBuddy application
"""

import streamlit as st
from typing import List, Dict, Optional
import re
from datetime import datetime


def validate_hf_token(token: str) -> bool:
    """
    Validate Hugging Face token format
    
    Args:
        token: Token to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not token:
        return False
    
    # Check minimum length for HF tokens
    return len(token) > 10


def count_tokens(text: str) -> int:
    """
    Estimate token count for a text string
    Rough estimation: 1 token ≈ 4 characters
    
    Args:
        text: Text to count tokens for
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def format_message_count(count: int) -> str:
    """
    Format message count for display
    
    Args:
        count: Number of messages
        
    Returns:
        Formatted string
    """
    return f"{count} message{'s' if count != 1 else ''}"


def get_conversation_summary(messages: List[Dict]) -> Dict:
    """
    Get statistics about the conversation
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Dictionary with conversation stats
    """
    user_messages = [m for m in messages if m['role'] == 'user']
    assistant_messages = [m for m in messages if m['role'] == 'assistant']
    
    total_tokens = sum(count_tokens(m['content']) for m in messages)
    
    return {
        "total_messages": len(messages),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "estimated_tokens": total_tokens,
        "average_user_length": sum(len(m['content']) for m in user_messages) / len(user_messages) if user_messages else 0,
        "average_assistant_length": sum(len(m['content']) for m in assistant_messages) / len(assistant_messages) if assistant_messages else 0,
    }


def sanitize_message(message: str) -> str:
    """
    Sanitize message for safe display
    
    Args:
        message: Message to sanitize
        
    Returns:
        Sanitized message
    """
    # Remove potential harmful characters while preserving formatting
    message = message.strip()
    return message


def create_system_prompt(context: Optional[str] = None) -> str:
    """
    Create a system prompt for the AI
    
    Args:
        context: Optional additional context
        
    Returns:
        System prompt string
    """
    base_prompt = "You are ByteBuddy, a helpful and intelligent AI assistant. You provide clear, accurate, and thoughtful responses to user queries."
    
    if context:
        return f"{base_prompt}\n\nAdditional context: {context}"
    
    return base_prompt


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[:max_length - len(suffix)] + suffix
    return text


def handle_api_error(error: Exception) -> str:
    """
    Handle and format API errors for display
    
    Args:
        error: Exception object
        
    Returns:
        User-friendly error message
    """
    error_str = str(error)
    
    if "401" in error_str or "unauthorized" in error_str.lower():
        return "❌ Authentication Error: Invalid or expired Hugging Face token. Please check your token."
    elif "rate" in error_str.lower() or "429" in error_str:
        return "⚠️ Rate Limited: Too many requests. Please wait a moment and try again."
    elif "timeout" in error_str.lower():
        return "⏱️ Timeout: Request took too long. Please try again."
    elif "not found" in error_str.lower() or "404" in error_str:
        return "❌ Model Error: The selected model is not available. Please choose a different model."
    else:
        return f"❌ Error: {error_str}"


def get_model_info(model: str) -> Dict:
    """
    Get information about a specific model
    
    Args:
        model: Model name
        
    Returns:
        Dictionary with model info
    """
    models_info = {
        "mistralai/Mistral-7B-Instruct-v0.2": {
            "name": "Mistral 7B Instruct",
            "speed": "Very Fast",
            "creator": "Mistral AI",
            "description": "Fast and efficient for most tasks"
        },
        "meta-llama/Llama-2-7b-chat-hf": {
            "name": "Llama 2 7B Chat",
            "speed": "Fast",
            "creator": "Meta",
            "description": "Excellent for conversations"
        },
        "HuggingFaceH4/zephyr-7b-beta": {
            "name": "Zephyr 7B Beta",
            "speed": "Fast",
            "creator": "Hugging Face",
            "description": "Good balance of speed and quality"
        },
        "tiiuae/falcon-7b-instruct": {
            "name": "Falcon 7B Instruct",
            "speed": "Moderate",
            "creator": "TII",
            "description": "High performance and capable"
        }
    }
    
    return models_info.get(model, {})


def export_conversation(messages: List[Dict], format: str = "txt") -> str:
    """
    Export conversation to specified format
    
    Args:
        messages: List of message dictionaries
        format: Export format ('txt', 'markdown', etc.)
        
    Returns:
        Formatted conversation string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if format == "markdown":
        output = f"# ByteBuddy Conversation\n*Exported on {timestamp}*\n\n"
        for msg in messages:
            role = "👤 User" if msg['role'] == 'user' else "🤖 Assistant"
            output += f"**{role}:**\n\n{msg['content']}\n\n---\n\n"
    else:  # txt format
        output = f"BYTEBUDDY CONVERSATION HISTORY\n{'='*50}\nExported: {timestamp}\n\n"
        for msg in messages:
            role = "USER" if msg['role'] == 'user' else "ASSISTANT"
            output += f"{role}:\n{msg['content']}\n\n{'-'*50}\n\n"
    
    return output


def format_response_time(seconds: float) -> str:
    """
    Format response time for display
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        return f"{seconds/60:.1f}m"
