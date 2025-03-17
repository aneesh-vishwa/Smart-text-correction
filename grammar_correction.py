import spacy

class GrammarCorrection:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    def correct_grammar(self, sentence):
        doc = self.nlp(sentence)
        corrected_sentence = []
        for token in doc:
            if token.dep_ == "aux" and token.head.tag_ == "VB":
                corrected_sentence.append(token.text + "s")  # Simple verb agreement fix
            else:
                corrected_sentence.append(token.text)
        return " ".join(corrected_sentence)
