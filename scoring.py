import re

# ---------- Utility functions ----------

def word_count(text):
    return len(text.split())

def sentence_count(text):
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])

def avg_sentence_length(text):
    wc = word_count(text)
    sc = sentence_count(text)
    return wc / sc if sc > 0 else 0

def has_dates(text):
    return bool(re.search(r'\b(19|20)\d{2}\b', text))

def has_cause_effect(text):
    keywords = ["because", "therefore", "following", "leading to", "as a result", "after"]
    return any(k in text.lower() for k in keywords)

def has_entities(text):
    # crude check for proper nouns
    return len(re.findall(r'\b[A-Z][a-z]+\b', text)) >= 5


# ---------- Scoring functions ----------

def content_and_structure_score(text):
    score = 20  # base for having meaningful content

    if sentence_count(text) >= 3:
        score += 5

    if has_dates(text):
        score += 5

    if has_cause_effect(text):
        score += 5

    if has_entities(text):
        score += 5

    return min(score, 40)


def speech_rate_score(text):
    """
    No audio available → measure sentence flow instead
    """
    avg_len = avg_sentence_length(text)

    if 12 <= avg_len <= 25:
        return 8
    elif 8 <= avg_len < 12 or 25 < avg_len <= 30:
        return 6
    else:
        return 4


def language_and_grammar_score(text):
    score = 20

    # Penalize obvious issues only
    if text.isupper():
        score -= 5

    if "  " in text:
        score -= 2

    if sentence_count(text) == 0:
        score -= 10

    return max(14, min(score, 20))


def clarity_score(text):
    avg_len = avg_sentence_length(text)

    if avg_len <= 25:
        return 15
    elif avg_len <= 30:
        return 13
    else:
        return 10


def engagement_score(text):
    score = 8  # minimum for informative speech

    if "?" in text:
        score += 2

    examples = ["for example", "such as", "for instance"]
    if any(e in text.lower() for e in examples):
        score += 2

    emphasis = ["important", "significant", "major", "key", "critical"]
    if any(w in text.lower() for w in emphasis):
        score += 3

    return min(score, 15)


# ---------- Final score ----------

def calculate_simplified_final_score(text):
    cs = content_and_structure_score(text)
    sr = speech_rate_score(text)
    lg = language_and_grammar_score(text)
    cl = clarity_score(text)
    eg = engagement_score(text)

    total = cs + sr + lg + cl + eg
    return round(total, 2)
