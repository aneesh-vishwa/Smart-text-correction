from collections import Counter
import math as calc

class nGram:
    def __init__(self, uni=False, bi=False, tri=False, quadri=False, penti=False):
        self.words = self.loadCorpus()
        if uni: self.unigram = self.createUnigram(self.words)
        if bi: self.bigram = self.createBigram(self.words)
        if tri: self.trigram = self.createTrigram(self.words)
        return

    def loadCorpus(self):
        print("Loading Corpus from data file")
        corpusfile = open('corpus.data', 'r')
        corpus = corpusfile.read()
        corpusfile.close()
        print("Processing Corpus")
        words = corpus.split(' ')
        return words
    
    def createUnigram(self, words):
        print("Creating Unigram Model")
        unigram = Counter(words)
        return unigram

    def createBigram(self, words):
        print("Creating Bigram Model")
        biwords = []
        for index, item in enumerate(words):
            if index == len(words) - 1:
                break
            biwords.append(item + ' ' + words[index + 1])
        print("Calculating Count for Bigram Model")
        bigram = Counter(biwords)
        return bigram

    def createTrigram(self, words):
        print("Creating Trigram Model")
        triwords = []
        for index, item in enumerate(words):
            if index == len(words) - 2:
                break
            triwords.append(item + ' ' + words[index + 1] + ' ' + words[index + 2])
        print("Calculating Count for Trigram Model")
        trigram = Counter(triwords)
        return trigram

    def probability(self, word, words="", gram='uni'):
        if gram == 'uni':
            return calc.log((self.unigram[word] + 1) / (len(self.words) + len(self.unigram)))
        elif gram == 'bi':
            return calc.log((self.bigram[words] + 1) / (self.unigram[word] + len(self.unigram)))
        elif gram == 'tri':
            return calc.log((self.trigram[words] + 1) / (self.bigram[word] + len(self.unigram)))
       
    def sentenceprobability(self, sent, gram='uni', form='antilog'):
        words = sent.lower().split()
        P = 0
        if gram == 'uni':
            for index, item in enumerate(words):
                P = P + self.probability(item)
        if gram == 'bi':
            for index, item in enumerate(words):
                if index == len(words) - 1:
                    break
                P = P + self.probability(item, item + ' ' + words[index + 1], 'bi')
        if gram == 'tri':
            for index, item in enumerate(words):
                if index == len(words) - 2:
                    break
                P = P + self.probability(item + ' ' + words[index + 1], item + ' ' + words[index + 1] + ' ' + words[index + 2], 'tri')
        if form == 'log':
            return P
        elif form == 'antilog':
            return calc.pow(calc.e, P)
