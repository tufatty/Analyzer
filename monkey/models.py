from django.db import models

class StringEntry(models.Model):
    value = models.CharField(max_length=255, unique=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField(default=False)
    is_natural = models.BooleanField(default=False)
    vowels = models.IntegerField(default=0)
    consonants = models.IntegerField(default=0)

    def __str__(self):
        return self.value
