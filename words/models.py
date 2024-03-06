from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError


# Only choices the part_of_speech field can be
PART_OF_SPEECH_CHOICES = {
    "n": "noun",
    "v": "verb",
    "adj": "adjective",
    "adv": "adverb",
    "pron": "pronoun",
    "prep": "preposition",
    "conj": "conjunction",
    "interj": "interjection"
}


# This model is to represent a conjugation for either present, past, or future
class Conjugation(models.Model):
    tagalog = models.CharField()
    english = models.CharField()
    accents = ArrayField(models.IntegerField())


# This model is to represent Conjugations for words that are verbs
class ConjugationSet(models.Model):
    present = models.OneToOneField(Conjugation)
    past = models.OneToOneField(Conjugation)
    future = models.OneToOneField(Conjugation)


# The model is for Word data objects
class Word(models.Model):
    tagalog = models.CharField()
    english = ArrayField(models.CharField(max_length=20)) # Tagalog words can have multiple english meanings
    root = models.CharField(max_length=20)
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH_CHOICES)
    conjugations = models.OneToOneField(ConjugationSet)
    note = models.CharField(max_length=255, blank=True)
    accents = ArrayField(models.IntegerField(), blank=True, null=True) # Optional array of integers
    audio = models.URLField(blank=True, null=True)

    # This method returns a string containing the english and tagalog translation
    def __str__(self):
        return f"{self.english} ({self.tagalog})"
    

    # This function checks for conjugations if the word is a verb
    def validate_verb_case(self):
        if self.part_of_speech == "verb" and self.conjugations == None:
            raise ValidationError("Verbs must have conjugations")


    # Overwriting the clean function to check if word is a verb
    def clean(self):
        self.validate_verb_case()
        return super().clean()
