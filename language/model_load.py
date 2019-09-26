#import en_core_web_sm 
#nlp=en_core_web_sm.load()
import spacy
#nlp = spacy.load('en_core_web_sm')
#nlp = en_core_web_sm.load()
nlp = spacy.load('en')
doc = nlp(u'This is a sentence.')
