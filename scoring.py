# scoring.py
import re
from textblob import TextBlob
import math
import nltk
import os

# Function to ensure NLTK data is available
def ensure_nltk_data():
    try:
        # Check if punkt tokenizer is available
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        # Download if not available
        nltk.download('punkt', quiet=True)
    
    try:
        # Check if averaged_perceptron_tagger is available
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        # Download if not available
        nltk.download('averaged_perceptron_tagger', quiet=True)

def improved_grammar_score(text):
    """More comprehensive grammar evaluation"""
    ensure_nltk_data()
    
    try:
        sentences = nltk.sent_tokenize(text)
    except:
        # Fallback if NLTK fails
        sentences = text.split('. ')
    
    if not sentences:
        return 0
    
    grammar_issues = 0
    
    # Check for sentence structure variety
    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    if len(set(sentence_lengths)) < 2:  # All sentences have similar length
        grammar_issues += 1
    
    # Check for proper capitalization
    for sentence in sentences:
        if sentence and not sentence[0].isupper():
            grammar_issues += 1
    
    # Check for proper punctuation
    if not re.search(r'[.!?]$', text):
        grammar_issues += 1
    
    # Convert to score (max 10)
    return max(0, 10 - min(grammar_issues, 10))

def vocabulary_richness(text):
    """Evaluate vocabulary diversity"""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    
    # Type-Token Ratio
    ttr = len(set(words)) / len(words)
    
    # Adjust for text length (longer texts naturally have lower TTR)
    adjusted_ttr = ttr * math.log(len(words) + 1)
    
    # Map to score (max 10)
    if adjusted_ttr > 2.5:
        return 10
    elif adjusted_ttr > 2.0:
        return 8
    elif adjusted_ttr > 1.5:
        return 6
    elif adjusted_ttr > 1.0:
        return 4
    else:
        return 2

def sentence_complexity(text):
    """Evaluate sentence structure complexity"""
    ensure_nltk_data()
    
    try:
        sentences = nltk.sent_tokenize(text)
    except:
        # Fallback if NLTK fails
        sentences = text.split('. ')
    
    if not sentences:
        return 0
    
    # Calculate average sentence length
    avg_length = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
    
    # Count different sentence structures
    complex_sentences = 0
    
    for sentence in sentences:
        words = sentence.split()
        
        # Count subordinate conjunctions as indicators of complex sentences
        sub_conj = ['that', 'which', 'who', 'whom', 'whose', 'where', 'when', 
                   'if', 'unless', 'because', 'since', 'although', 'while']
        
        if any(word.lower() in sub_conj for word in words):
            complex_sentences += 1
    
    # Calculate complexity score
    if avg_length > 20 and complex_sentences > 0:
        return 10
    elif avg_length > 15 and complex_sentences > 0:
        return 8
    elif avg_length > 10:
        return 6
    else:
        return 4

def coherence_score(text):
    """Evaluate text coherence through transition words and logical flow"""
    # List of transition words
    transitions = [
        'however', 'therefore', 'consequently', 'furthermore', 'moreover', 
        'nevertheless', 'nonetheless', 'meanwhile', 'otherwise', 'thus',
        'hence', 'accordingly', 'additionally', 'also', 'as a result',
        'for example', 'for instance', 'in fact', 'in addition', 'in conclusion',
        'first', 'second', 'third', 'finally', 'next', 'then', 'afterward'
    ]
    
    words = re.findall(r'\b\w+\b', text.lower())
    transition_count = sum(1 for word in words if word in transitions)
    
    # Calculate transition density
    if not words:
        return 0
    transition_density = transition_count / len(words)
    
    # Map to score (max 10)
    if transition_density > 0.05:
        return 10
    elif transition_density > 0.03:
        return 8
    elif transition_density > 0.01:
        return 6
    else:
        return 4

def clarity_score(text):
    """Evaluate text clarity through filler words and conciseness"""
    filler_words = ["like", "um", "uh", "basically", "actually", "you know", 
                   "sort of", "kind of", "I mean", "well", "so", "anyway"]
    
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    
    filler_count = sum(1 for word in words if word in filler_words)
    filler_ratio = filler_count / len(words)
    
    # Check for conciseness (ratio of content words to total words)
    content_words = [w for w in words if w not in 
                    ['a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 
                     'are', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 
                     'does', 'did', 'will', 'would', 'could', 'should']]
    
    if not words:
        content_ratio = 0
    else:
        content_ratio = len(content_words) / len(words)
    
    # Calculate clarity score (max 15)
    filler_score = max(0, 7 - filler_ratio * 100)
    content_score = content_ratio * 8
    
    return min(15, filler_score + content_score)

def engagement_score(text):
    """Evaluate engagement through varied factors"""
    # Sentiment analysis
    try:
        polarity = TextBlob(text).sentiment.polarity
    except:
        # Fallback if TextBlob fails
        polarity = 0
    
    # Check for rhetorical questions
    rhetorical_questions = len(re.findall(r'\?', text))
    
    # Calculate engagement score (max 15)
    sentiment_score = 5 + abs(polarity) * 5  # Both positive and negative can be engaging
    question_score = min(5, rhetorical_questions * 2)
    
    return min(15, sentiment_score + question_score)

def content_relevance_score(text):
    """Evaluate content quality based on information density"""
    # Count numbers/dates which often indicate specific information
    numbers = len(re.findall(r'\b\d+\b', text))
    
    # Calculate information density
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    
    # Count capitalized words which might indicate proper nouns/entities
    capitalized_words = [word for word in text.split() if word and word[0].isupper()]
    unique_entities = len(set(capitalized_words))
    
    info_density = (unique_entities + numbers) / len(words)
    
    # Map to score (max 20)
    if info_density > 0.15:
        return 20
    elif info_density > 0.10:
        return 15
    elif info_density > 0.05:
        return 10
    else:
        return 5

def structure_score(text):
    """Evaluate speech structure"""
    ensure_nltk_data()
    
    try:
        sentences = nltk.sent_tokenize(text)
    except:
        # Fallback if NLTK fails
        sentences = text.split('. ')
    
    if not sentences:
        return 0
    
    # Check for introduction and conclusion
    intro_indicators = ['introduction', 'today', 'in this', 'i will', 'we will', 'let me']
    conclusion_indicators = ['conclusion', 'in conclusion', 'finally', 'in summary', 'to summarize']
    
    has_intro = any(indicator in text.lower() for indicator in intro_indicators)
    has_conclusion = any(indicator in text.lower() for indicator in conclusion_indicators)
    
    # Check for logical progression (simplified)
    # We'll check if there's a reasonable flow from general to specific or vice versa
    first_sentence = sentences[0].lower()
    last_sentence = sentences[-1].lower()
    
    # Simple heuristic: first sentence should introduce topic, last should summarize
    first_has_topic = any(word in first_sentence for word in ['this', 'today', 'we', 'i', 'here'])
    last_has_summary = any(word in last_sentence for word in ['therefore', 'thus', 'in conclusion', 'finally'])
    
    structure_points = 0
    if has_intro:
        structure_points += 5
    if has_conclusion:
        structure_points += 5
    if first_has_topic:
        structure_points += 5
    if last_has_summary:
        structure_points += 5
    
    return min(20, structure_points)

def calculate_improved_score(text):
    """Calculate the overall speech score using improved metrics"""
    # Component scores with their maximum values
    grammar = improved_grammar_score(text)                # Max: 10
    vocab = vocabulary_richness(text)                     # Max: 10
    complexity = sentence_complexity(text)                # Max: 10
    coherence = coherence_score(text)                     # Max: 10
    clarity = clarity_score(text)                         # Max: 15
    engagement = engagement_score(text)                   # Max: 15
    content = content_relevance_score(text)               # Max: 20
    structure = structure_score(text)                     # Max: 20
    
    # Calculate total score
    total_score = grammar + vocab + complexity + coherence + clarity + engagement + content + structure
    
    return total_score, {
        "Grammar": grammar,
        "Vocabulary": vocab,
        "Sentence Complexity": complexity,
        "Coherence": coherence,
        "Clarity": clarity,
        "Engagement": engagement,
        "Content Relevance": content,
        "Structure": structure
    }

def main():
    print("Welcome to the Improved Speech Evaluation System")
    print("Paste your entire speech below and press Enter twice or type 'END' to finish:")
    
    try:
        text = []
        empty_lines = 0
        while True:
            try:
                line = input()
                if line.strip().upper() == 'END':
                    break
                if not line.strip():
                    empty_lines += 1
                    if empty_lines >= 1:  # Changed from 2 to 1 for single Enter
                        break
                    text.append('')  # Keep single empty lines in the text
                    continue
                else:
                    empty_lines = 0
                    text.append(line)
            except EOFError:
                break
        
        text = '\n'.join(text)
        
        if not text.strip():
            print("No text entered. Exiting...")
            return
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return
    
    score, breakdown = calculate_improved_score(text)
    print("\n--- Evaluation Results ---")
    print(f"Your speech score: {score:.1f}/100")
    print("\nBreakdown:")
    for category, points in breakdown.items():
        print(f"- {category}: {points:.1f}")
    
    # Add qualitative feedback
    print("\n--- Feedback ---")
    if score >= 80:
        print("Excellent speech! Well-structured and engaging.")
    elif score >= 60:
        print("Good speech with room for improvement in some areas.")
    elif score >= 40:
        print("Fair speech. Consider working on structure and clarity.")
    else:
        print("The speech needs significant improvement in multiple areas.")

if __name__ == "__main__":
    main()
