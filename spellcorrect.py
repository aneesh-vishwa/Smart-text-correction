

from __future__ import division
import ast
from ngram import nGram
import math as calc
import json

class SpellCorrect():
    def __init__(self):
        self.ng = nGram(True, True, False, False, False)
        self.words = sorted(set(self.ng.words))  # Include all words
        self.loadConfusionMatrix()
        self.dict = self.loadDict()
        return

    def loadConfusionMatrix(self):
        """Loads confusion matrices from JSON files."""
        self.confusion_matrices = {}
        for error_type in ['add', 'sub', 'del', 'rev']:
            try:
                with open(f'{error_type}confusion_cleaned.json', 'r') as f:
                    self.confusion_matrices[error_type] = json.load(f)
            except FileNotFoundError:
                self.confusion_matrices[error_type] = {}
    
    def loadDict(self):
        with open('dictionary.data', 'r') as f:
            return set(f.read().split("\n"))  # Use a set for fast lookup
    
    def dl(self, s1, s2):
        s1, s2 = '#' + s1, '#' + s2
        m, n = len(s1), len(s2)
        D = [[0]*n for _ in range(m)]
        
        for i in range(m):
            D[i][0] = i
        for j in range(n):
            D[0][j] = j
        
        for i in range(1, m):
            for j in range(1, n):
                cost = 0 if s1[i] == s2[j] else 1
                D[i][j] = min(D[i-1][j] + 1, D[i][j-1] + 1, D[i-1][j-1] + cost)
        
        return D[m-1][n-1]

    def genCandidates(self, word):
        candidates = {item: self.dl(word, item) for item in self.words if self.dl(word, item) <= 3}
        return sorted(candidates, key=candidates.get)[:5]  # Return top 5
    
    def correct_word(self, word):
        if word in self.dict:
            return word  # Return if it's already correct
        
        suggestions = self.genCandidates(word)
        
        if not suggestions:
            print(f"No suggestions found for: {word}")
            return input(f"Enter the correct spelling for '{word}': ")
        
        print(f"Possible corrections for '{word}':")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}: {suggestion}")
        
        choice = input("Choose the correct word (or type manually): ")
        return suggestions[int(choice) - 1] if choice.isdigit() and 1 <= int(choice) <= len(suggestions) else choice.strip()
    
    def spell_check(self, text):
        words = text.split()
        corrected_words = []
        
        print("\nSpell Checking Sentence...")
        for word in words:
            if word not in self.dict:
                corrected_word = self.correct_word(word)
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        
        corrected_sentence = ' '.join(corrected_words)
        print("\nFinal Corrected Text:", corrected_sentence)
        return corrected_sentence

if __name__ == "__main__":
    spell_checker = SpellCorrect()
    text = input("Enter text to check spelling: ")
    spell_checker.spell_check(text)
