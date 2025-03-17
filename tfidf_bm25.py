import math
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

class TFIDF_BM25:
    def __init__(self, words):
        self.words = words
        self.word_frequencies = Counter(words)
        self.tfidf_vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform([" ".join(words)])
    
    def compute_bm25(self, word, k1=1.5, b=0.75):
        best_match = word
        max_score = -1
        avg_doc_length = np.mean([len(w) for w in self.words])
        
        for candidate in set(self.words):
            f = self.word_frequencies[candidate]
            idf = math.log((len(self.words) - f + 0.5) / (f + 0.5) + 1)
            score = idf * ((f * (k1 + 1)) / (f + k1 * (1 - b + b * (len(candidate) / avg_doc_length))))
            
            if score > max_score:
                max_score = score
                best_match = candidate
        
        return best_match
    
    def compute_tfidf_similarity(self, word):
        word_vector = self.tfidf_vectorizer.transform([word])
        similarities = (self.tfidf_matrix * word_vector.T).toarray()
        best_match_index = similarities.argmax()
        return self.words[best_match_index]
