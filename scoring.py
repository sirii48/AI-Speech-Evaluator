import nltk
nltk.download('punkt', quiet=True)
nltk.download('brown', quiet=True)
nltk.download('wordnet', quiet=True)

import re
from textblob import TextBlob

def count_grammar_errors(text):
    # Very simple placeholder grammar check
    # You can replace with LanguageTool or Ginger API later
    blob = TextBlob(text)
    errors = 0
    for sentence in blob.sentences:
        corrected = sentence.correct()
        if corrected != sentence:
            errors += 1
    return errors


def type_token_ratio(text):
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0
    return len(set(words)) / len(words)


def count_filler_words(text):
    fillers = ["like", "um", "uh", "basically", "actually", "you know"]
    text_low = text.lower()
    count = 0
    for f in fillers:
        count += text_low.count(f)
    return count


def sentiment_score(text):
    return TextBlob(text).sentiment.polarity


def content_and_structure_score(text):
    score = 0
    text_low = text.lower()

    # 1. Salutation
    if text_low.startswith(("hello", "hi", "good morning", "good afternoon", "good evening")):
        score += 5

    # 2. Keywords (8 keywords * 2.5 = 20)
    keywords = ["name", "age", "class", "school", "family", "hobby", "interest", "goal", "ambition", "unique"]
    kw_score = 0
    for kw in keywords:
        if kw in text_low:
            kw_score += 2.5
            if kw_score > 20:
                kw_score = 20
    score += kw_score

    # 3. Flow check
    # Sequence: name → background → hobbies → closing
    has_name = "my name" in text_low or "i am" in text_low
    has_background = any(w in text_low for w in ["age", "class", "school"])
    has_hobbies = any(w in text_low for w in ["hobby", "hobbies", "interest"])
    has_closing = any(w in text_low for w in ["thank you", "that's all"])

    if has_name and has_background and has_hobbies and has_closing:
        score += 15
    elif has_name and has_background:
        score += 10
    else:
        score += 5

    # Max raw = 40
    return min(score, 40)


def speech_rate_score(text):
    words = len(text.split())

    if 110 <= words <= 160:
        return 10
    elif 90 <= words < 110 or 160 < words <= 190:
        return 7
    else:
        return 4


def language_and_grammar_score(text):
    errors = count_grammar_errors(text)

    # Grammar score
    if errors < 3:
        grammar_score = 10
    elif errors <= 6:
        grammar_score = 7
    else:
        grammar_score = 4

    # Vocabulary richness
    ttr = type_token_ratio(text)
    if ttr > 0.45:
        vocab_score = 10
    elif ttr > 0.30:
        vocab_score = 7
    else:
        vocab_score = 4

    return grammar_score + vocab_score  # max = 20


def clarity_score(text):
    fillers = count_filler_words(text)

    if fillers <= 2:
        return 15
    elif fillers <= 5:
        return 10
    else:
        return 5


def engagement_score(text):
    polarity = sentiment_score(text)

    if polarity > 0.2:
        return 15
    elif polarity >= 0:
        return 10
    else:
        return 5


def calculate_simplified_final_score(text):
    score = 0

    score += content_and_structure_score(text)     # 40
    score += speech_rate_score(text)               # 10
    score += language_and_grammar_score(text)      # 20
    score += clarity_score(text)                   # 15
    score += engagement_score(text)                # 15

    return score  # Already out of 100


def main():
    print("Welcome to the Speech Evaluation System")
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
    
    score = calculate_simplified_final_score(text)
    print("\n--- Evaluation Results ---")
    print(f"Your speech score: {score:.1f}/100")
    print("\nBreakdown:")
    print(f"- Content & Structure: {content_and_structure_score(text)}/40")
    print(f"- Speech Rate: {speech_rate_score(text)}/10")
    print(f"- Language & Grammar: {language_and_grammar_score(text)}/20")
    print(f"- Clarity: {clarity_score(text)}/15")
    print(f"- Engagement: {engagement_score(text)}/15")


if __name__ == "__main__":
    main()