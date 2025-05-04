import pytest
from moderation import check_content, MIN_CONTENT_LENGTH, MAX_CONTENT_LENGTH, BANNED_WORDS

def test_content_length_validation():
    # Test content that is too short
    short_content = "This is too short."
    result = check_content(short_content)
    assert not result["approved"]
    assert any("too short" in reason for reason in result["reasons"])
    
    # Test content that is too long
    long_content = "a" * (MAX_CONTENT_LENGTH + 1)
    result = check_content(long_content)
    assert not result["approved"]
    assert any("too long" in reason for reason in result["reasons"])
    
    # Test content with valid length
    valid_content = "a" * MIN_CONTENT_LENGTH
    result = check_content(valid_content)
    assert result["approved"]

def test_banned_words_detection():
    # Test content with banned words
    for banned_word in BANNED_WORDS[:3]:  # Test first 3 banned words
        content = f"This is a test post containing the word {banned_word} which should be flagged."
        result = check_content(content)
        assert not result["approved"]
        assert any("Banned words" in reason for reason in result["reasons"])
        assert banned_word in str(result["reasons"])
    
    # Test content without banned words
    clean_content = "This is a completely clean post with appropriate content and sufficient length to pass the minimum requirements."
    result = check_content(clean_content)
    assert result["approved"]

def test_tone_detection():
    # Test aggressive tone (all caps)
    aggressive_content = "THIS IS AN AGGRESSIVE POST THAT SHOULD BE FLAGGED FOR TONE. " + "a" * (MIN_CONTENT_LENGTH - 60)
    result = check_content(aggressive_content)
    assert not result["approved"]
    assert any("tone" in reason.lower() for reason in result["reasons"])
    
    # Test excessive exclamation marks
    exclamation_content = "This post has too many exclamation marks!!!!! It should be flagged!!! Right?!!!! " + "a" * (MIN_CONTENT_LENGTH - 80)
    result = check_content(exclamation_content)
    assert not result["approved"]
    assert any("tone" in reason.lower() for reason in result["reasons"])
    
    # Test normal tone
    normal_content = "This is a normally toned post with appropriate language and sufficient length to meet the requirements."
    normal_content += " " * (MIN_CONTENT_LENGTH - len(normal_content))
    result = check_content(normal_content)
    assert result["approved"]

def test_multiple_issues():
    # Test content with multiple issues (short and banned words)
    bad_content = f"This is {BANNED_WORDS[0]}"
    result = check_content(bad_content)
    assert not result["approved"]
    assert len(result["reasons"]) >= 2  # Should have at least 2 reasons
    
    # Test all possible violations
    terrible_content = f"THIS IS TERRIBLE!!! {BANNED_WORDS[0]} AND {BANNED_WORDS[1]}!!!"
    result = check_content(terrible_content)
    assert not result["approved"]
    assert len(result["reasons"]) >= 3  # Should have multiple reasons

def test_title_moderation():
    # Test all caps title
    result = check_content("This is normal content that is long enough to pass the length check." + "a" * 30, "THIS IS AN ANGRY TITLE")
    assert not result["approved"]
    assert any("title" in reason.lower() for reason in result["reasons"])
    
    # Test normal title
    result = check_content("This is normal content that is long enough to pass the length check." + "a" * 30, "This is a normal title")
    assert result["approved"]
