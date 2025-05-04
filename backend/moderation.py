import re
from typing import Dict, List, Any

# Sample list of banned words (in a real scenario, this could be loaded from a file or a database)
BANNED_WORDS = [
    "profanity", "insult", "stupid", "idiot", "moron", "hate", 
    "dumb", "damn", "hell", "jerk", "ass", "crap", "shit"
]

# Minimum and maximum content length
MIN_CONTENT_LENGTH = 50
MAX_CONTENT_LENGTH = 2000

def check_content(content: str, title: str = "") -> Dict[str, Any]:
    """
    Simulates AI moderation by checking content against predefined rules.
    
    Args:
        content: The post content to check
        title: The post title (optional for additional checks)
        
    Returns:
        A dict with 'approved' flag and list of 'reasons' if not approved
    """
    reasons = []
    
    # Check content length
    if len(content) < MIN_CONTENT_LENGTH:
        reasons.append(f"Content too short (minimum {MIN_CONTENT_LENGTH} characters)")
    elif len(content) > MAX_CONTENT_LENGTH:
        reasons.append(f"Content too long (maximum {MAX_CONTENT_LENGTH} characters)")
    
    # Check for banned words
    banned_words_found = [word for word in BANNED_WORDS if word.lower() in content.lower()]
    if banned_words_found:
        reasons.append(f"Banned words detected: {', '.join(banned_words_found)}")
    
    # Check for aggressive tone (all caps)
    words = content.split()
    all_caps_words = [word for word in words if word.isupper() and len(word) > 2]
    if len(all_caps_words) > 3 or (len(all_caps_words) / len(words) > 0.2 and len(words) > 10):
        reasons.append("Aggressive tone detected (excessive use of capital letters)")
    
    # Check for aggressive punctuation
    if content.count('!') > 5:
        reasons.append("Aggressive tone detected (excessive exclamation marks)")
    
    # Check if title is all caps (if provided)
    if title and title.isupper() and len(title) > 5:
        reasons.append("Aggressive tone in title (all capital letters)")
    
    # Advanced pattern matching to detect aggressive language patterns
    if re.search(r'(\?{3,}|\!{3,})', content):
        reasons.append("Aggressive tone detected (excessive punctuation)")
    
    # Final result
    return {
        "approved": len(reasons) == 0,
        "reasons": reasons
    }
