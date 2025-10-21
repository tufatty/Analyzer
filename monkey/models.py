# A String Analyzer API (using Django REST Framework)

from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.urls import path
import hashlib, json
from collections import Counter
# Create your models here.


# ========================
# MODELS
# ========================
class StringEntry(models.Model):
    id = models.CharField(max_length=64, primary_key=True)  # sha256 hash
    value = models.TextField(unique=True)
    properties = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.value

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