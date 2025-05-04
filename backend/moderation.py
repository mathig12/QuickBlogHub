import re
import html
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Sample list of banned words (in a real scenario, this could be loaded from a file or a database)
BANNED_WORDS = [
    "profanity", "insult", "stupid", "idiot", "moron", "hate", 
    "dumb", "damn", "hell", "jerk", "ass", "crap", "shit",
    "fool", "bastard", "bitch", "asshole", "wtf", "bullshit",
    "retard", "retarded", "dumbass", "screw", "screwed"
]

# Context-specific inappropriate phrases
INAPPROPRIATE_PHRASES = [
    "shut up",
    "get lost",
    "go to hell",
    "you suck",
    "loser",
    "screw you",
    "I hate",
    "worst ever",
    "waste of time",
    "complete garbage"
]

# Suspicious patterns that might indicate problematic content
SUSPICIOUS_PATTERNS = [
    r'(\w+)\1{3,}',                   # Repeated characters (e.g., "hahahaha")
    r'[A-Z]{5,}',                     # Long sequences of caps
    r'!!+',                           # Multiple exclamation marks
    r'\?\?+',                         # Multiple question marks
    r'[!?]{4,}',                      # Multiple mixed punctuation
    r'(^|\s)[\w\.-]+@[\w\.-]+(\s|$)'  # Email addresses (privacy concern)
]

# Minimum and maximum content length
MIN_CONTENT_LENGTH = 50
MAX_CONTENT_LENGTH = 10000

# Content quality indicators
MIN_AVG_WORD_LENGTH = 3.0
MIN_UNIQUE_WORDS_RATIO = 0.4

# Sentiment indicators
NEGATIVE_SENTIMENT_WORDS = [
    "hate", "terrible", "awful", "horrible", "disgusting", "pathetic", 
    "useless", "waste", "stupid", "dumb", "idiot", "failure", "worst"
]

# Contextual patterns for offensive content
CONTEXTUAL_PATTERNS = {
    "harassment": [r"you (are|r) (an?)? ?(stupid|idiot|dumb|fool)", r"nobody (likes|cares about) you"],
    "threats": [r"(will|gonna|going to) (kill|hurt|harm)", r"watch (your|ur) back"],
    "discrimination": [r"(all|those) (people|guys|folks) (are|r) (stupid|dumb|evil|criminal)", r"(hate|despise) (all|those) (\w+)"]
}

# AI suggestion templates
TITLE_IMPROVEMENT_SUGGESTIONS = [
    "Consider using more specific language in your title to attract readers",
    "Your title could be more engaging by adding a compelling hook",
    "Try making your title more concise and impactful",
    "Consider adding a number or statistic to your title for better engagement",
    "A more descriptive title might help attract your target audience"
]

CONTENT_IMPROVEMENT_SUGGESTIONS = [
    "Your content could benefit from more specific examples",
    "Consider breaking up longer paragraphs for better readability",
    "Adding subheadings would improve the structure of your content",
    "Consider including more factual information to support your points",
    "Your content could be enhanced with additional evidence or statistics"
]

def strip_html(text: str) -> str:
    """Remove HTML tags from content for cleaner analysis."""
    # First unescape any HTML entities
    text = html.unescape(text)
    # Then remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text

def calculate_readability_score(text: str) -> float:
    """
    Calculate a simple readability score based on sentence and word length.
    Higher scores indicate more complex text.
    """
    # Remove HTML tags
    text = strip_html(text)
    
    # Split into sentences (simple approach)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0
    
    # Calculate average sentence length
    words = text.split()
    avg_sentence_length = len(words) / len(sentences)
    
    # Calculate average word length
    if not words:
        return 0
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / len(words)
    
    # Simple readability score (higher means more complex)
    return (avg_sentence_length * 0.6) + (avg_word_length * 0.4)

def analyze_content_quality(text: str) -> Dict[str, Any]:
    """Analyze the content quality and provide metrics."""
    # Remove HTML tags
    text = strip_html(text)
    
    # Basic word statistics
    words = [word.lower() for word in re.findall(r'\b\w+\b', text)]
    total_words = len(words)
    unique_words = len(set(words))
    
    if total_words == 0:
        return {
            "word_count": 0,
            "unique_words": 0,
            "unique_ratio": 0,
            "avg_word_length": 0,
            "readability_score": 0,
            "estimated_reading_time": 0
        }
    
    # Calculate metrics
    unique_ratio = unique_words / total_words
    avg_word_length = sum(len(word) for word in words) / total_words
    readability_score = calculate_readability_score(text)
    
    # Estimate reading time (average person reads ~200-250 words per minute)
    reading_time_minutes = max(1, round(total_words / 225))
    
    return {
        "word_count": total_words,
        "unique_words": unique_words,
        "unique_ratio": unique_ratio,
        "avg_word_length": avg_word_length,
        "readability_score": readability_score,
        "estimated_reading_time": reading_time_minutes
    }

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Simple sentiment analysis.
    In a real system, this would use a proper NLP model.
    """
    # Remove HTML tags
    text = strip_html(text).lower()
    
    # Count negative sentiment words
    negative_count = sum(1 for word in NEGATIVE_SENTIMENT_WORDS if word in text)
    
    # Simple sentiment score (-1 to 1)
    words = text.split()
    if not words:
        return {"sentiment_score": 0, "is_negative": False}
    
    sentiment_score = 1.0 - (negative_count * 2 / len(words))
    sentiment_score = max(-1.0, min(1.0, sentiment_score))  # Clamp between -1 and 1
    
    return {
        "sentiment_score": sentiment_score,
        "is_negative": sentiment_score < -0.3  # Threshold for negative sentiment
    }

def generate_improvement_suggestions(content: str, title: str = "") -> Dict[str, List[str]]:
    """Generate AI suggestions to improve the content and title."""
    suggestions = {"title": [], "content": []}
    
    # Title suggestions
    if title:
        if len(title) < 20:
            suggestions["title"].append("Your title is quite short. Consider making it more descriptive.")
        elif len(title) > 80:
            suggestions["title"].append("Your title is quite long. Consider making it more concise.")
        
        # Add a random title improvement suggestion
        suggestions["title"].append(random.choice(TITLE_IMPROVEMENT_SUGGESTIONS))
    
    # Content suggestions
    quality = analyze_content_quality(content)
    
    if quality["word_count"] < 200:
        suggestions["content"].append("Your content is relatively short. Consider adding more details or examples.")
    
    if quality["unique_ratio"] < MIN_UNIQUE_WORDS_RATIO:
        suggestions["content"].append("Your content has many repeated words. Consider using a more diverse vocabulary.")
    
    if quality["avg_word_length"] < MIN_AVG_WORD_LENGTH:
        suggestions["content"].append("Your content uses many short words. Consider incorporating more specific terminology.")
    
    # Structure suggestions
    paragraphs = re.split(r'\n\s*\n', strip_html(content))
    if len(paragraphs) < 3 and quality["word_count"] > 200:
        suggestions["content"].append("Consider breaking your content into more paragraphs for better readability.")
    
    # Add a random content improvement suggestion
    suggestions["content"].append(random.choice(CONTENT_IMPROVEMENT_SUGGESTIONS))
    
    return suggestions

def check_content(content: str, title: str = "") -> Dict[str, Any]:
    """
    Enhanced AI moderation by checking content against advanced rules.
    
    Args:
        content: The post content to check
        title: The post title (optional for additional checks)
        
    Returns:
        A dict with 'approved' flag, list of 'reasons' if not approved,
        and additional metadata including quality analysis and suggestions
    """
    # Remove HTML tags for analysis
    clean_content = strip_html(content)
    
    reasons = []
    warnings = []
    quality_score = 0
    
    # Check content length
    if len(clean_content) < MIN_CONTENT_LENGTH:
        reasons.append(f"Content too short (minimum {MIN_CONTENT_LENGTH} characters)")
    elif len(clean_content) > MAX_CONTENT_LENGTH:
        reasons.append(f"Content too long (maximum {MAX_CONTENT_LENGTH} characters)")
    
    # Check for banned words
    banned_words_found = [word for word in BANNED_WORDS if word.lower() in clean_content.lower()]
    if banned_words_found:
        reasons.append(f"Banned words detected: {', '.join(banned_words_found)}")
    
    # Check for inappropriate phrases
    inappropriate_phrases_found = [phrase for phrase in INAPPROPRIATE_PHRASES if phrase.lower() in clean_content.lower()]
    if inappropriate_phrases_found:
        reasons.append(f"Inappropriate phrases detected: {', '.join(inappropriate_phrases_found)}")
    
    # Check for suspicious patterns
    pattern_matches = []
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, clean_content):
            pattern_matches.append(pattern)
    
    if pattern_matches:
        warnings.append("Suspicious patterns detected in your content")
    
    # Check for aggressive tone (all caps)
    words = clean_content.split()
    if words:  # Prevent division by zero
        all_caps_words = [word for word in words if word.isupper() and len(word) > 2]
        if len(all_caps_words) > 3 or (len(all_caps_words) / len(words) > 0.2 and len(words) > 10):
            reasons.append("Aggressive tone detected (excessive use of capital letters)")
    
    # Check for aggressive punctuation
    if clean_content.count('!') > 5:
        warnings.append("Excessive exclamation marks detected")
    
    # Check if title is all caps (if provided)
    if title and title.isupper() and len(title) > 5:
        reasons.append("Aggressive tone in title (all capital letters)")
    
    # Check for contextual offensive patterns
    for context, patterns in CONTEXTUAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, clean_content, re.IGNORECASE):
                reasons.append(f"Potential {context} content detected")
                break
    
    # Analyze quality and sentiment
    quality = analyze_content_quality(clean_content)
    sentiment = analyze_sentiment(clean_content)
    
    # Quality checks
    if quality["unique_ratio"] < MIN_UNIQUE_WORDS_RATIO and quality["word_count"] > 100:
        warnings.append("Low vocabulary diversity")
    
    # Sentiment check
    if sentiment["is_negative"]:
        warnings.append("Predominantly negative tone detected")
    
    # Calculate quality score (0-100)
    if quality["word_count"] > 0:
        quality_factors = [
            min(1.0, quality["word_count"] / 500) * 25,  # Word count factor
            min(1.0, quality["unique_ratio"] / 0.6) * 25,  # Uniqueness factor
            min(1.0, quality["avg_word_length"] / 5) * 25,  # Word complexity factor
            min(1.0, (sentiment["sentiment_score"] + 1) / 2) * 25  # Sentiment factor
        ]
        quality_score = sum(quality_factors)
    
    # Generate improvement suggestions
    suggestions = generate_improvement_suggestions(content, title)
    
    # Final result
    return {
        "approved": len(reasons) == 0,
        "reasons": reasons,
        "warnings": warnings,
        "quality_score": quality_score,
        "quality_analysis": quality,
        "sentiment_analysis": sentiment,
        "suggestions": suggestions,
        "moderation_timestamp": datetime.now().isoformat()
    }
