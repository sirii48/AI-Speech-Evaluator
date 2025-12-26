import nltk
import re
import textstat
from textblob import TextBlob

# Ensure necessary data is downloaded
nltk.download('punkt', quiet=True)

def type_token_ratio(text):
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    return len(set(words)) / len(words)

def count_filler_words(text):
    # Expanded filler list
    fillers = ["like", "um", "uh", "basically", "actually", "you know", "sort of"]
    text_low = text.lower()
    count = sum(text_low.count(f) for f in fillers)
    return count

def content_and_structure_score(text):
    """Grades based on information density and professional structure."""
    score = 0
    word_count = len(text.split())
    
    # 1. Length/Substance (20 pts)
    if word_count > 150: score += 20
    elif word_count > 75: score += 15
    else: score += 5

    # 2. Complexity/Structure (20 pts)
    # Using Coleman-Liau Index as a proxy for structural sophistication
    grade_level = textstat.coleman_liau_index(text)
    if grade_level >= 10: # High school/College level writing
        score += 20
    elif grade_level >= 7:
        score += 15
    else:
        score += 5

    return min(score, 40)

def speech_rate_score(text):
    """Evaluates the 'Tempo' based on word complexity."""
    # Ideal speeches have a mix of simple and complex words
    diff_words = textstat.difficult_words(text)
    total_words = len(text.split())
    ratio = diff_words / total_words if total_words > 0 else 0
    
    # If the text is too simple or too overly complex, score drops
    if 0.1 <= ratio <= 0.3:
        return 10
    elif ratio < 0.1:
        return 7
    else:
        return 5

def language_and_grammar_score(text):
    """Grades based on Vocabulary Richness and Readability."""
    # Vocabulary richness (TTR)
    ttr = type_token_ratio(text)
    vocab_score = 10 if ttr > 0.5 else (7 if ttr > 0.35 else 4)

    # Readability (Flesch Ease)
    ease = textstat.flesch_reading_ease(text)
    # 60-100 is standard clear speech
    grammar_score = 10 if ease > 50 else 7

    return grammar_score + vocab_score

def clarity_score(text):
    """Grades based on lack of filler words and sentence flow."""
    fillers = count_filler_words(text)
    avg_sentence_len = textstat.avg_sentence_length(text)

    score = 0
    # Filler penalty
    if fillers <= 2: score += 10
    else: score += 5
    
    # Flow (Avg sentence length between 10-20 words is ideal for speaking)
    if 10 <= avg_sentence_len <= 25: score += 5
    else: score += 2
    
    return min(score, 15)

def engagement_score(text):
    """Grades based on Sentiment and Subjectivity."""
    blob = TextBlob(text)
    polarity = abs(blob.sentiment.polarity) # Stronger emotions (pos or neg) are more engaging
    subjectivity = blob.sentiment.subjectivity # Opinions are more engaging than raw dry facts
    
    score = 5 # Base score
    if polarity > 0.1: score += 5
    if subjectivity > 0.3: score += 5
    
    return min(score, 15)

def calculate_simplified_final_score(text):
    return (
        content_and_structure_score(text) +
        speech_rate_score(text) +
        language_and_grammar_score(text) +
        clarity_score(text) +
        engagement_score(text)
    )
