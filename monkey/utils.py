import hashlib
from collections import Counter



# ========================
# UTILITY FUNCTIONS
# ========================
def analyze_string(value: str):
    length = len(value)
    is_palindrome = value.lower() == value[::-1].lower()
    unique_characters = len(set(value))
    word_count = len(value.split())
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    character_frequency_map = dict(Counter(value))

    return {
        'length': length,
        'is_palindrome': is_palindrome,
        'unique_characters': unique_characters,
        'word_count': word_count,
        'sha256_hash': sha256_hash,
        'character_frequency_map': character_frequency_map,
    }