from metaphone import doublemetaphone
from collections import Counter

class PhoneticCorrection:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.word_frequencies = Counter(dictionary)
    
    def correct_phonetic(self, word):
        phonetic_code = doublemetaphone(word)[0]
        candidates = [w for w in self.dictionary if doublemetaphone(w)[0] == phonetic_code]
        return max(candidates, key=self.word_frequencies.get, default=word)
