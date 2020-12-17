#Author: Vikram  Nimmakuri
#Licence: MIT

import re
import os
import sys

import numpy as np 
import pandas as pd 
import spacy
from spacy.lang.en.stop_words import STOP_WORDS as stopwords
from bs4 import BeautifulSoup
import unicodedata
from textblob import TextBlob

nlp = spacy.load('en_core_web_sm')

#Method for calculating no of words:
def _get_wordcounts(x):
	length = len(str(x).split())
	return length

#method for calculating no of characters:
def _get_charcounts(x):
	s = x.split()
	x = ''.join(s)
	return len(x)

#method for calculating avg of wordlenght:
def _get_avg_wordlength(x):
	count = _get_charcounts(x)/_get_wordcounts(x)
	return count

#method for calculating stopwords counts:
def _get_stopwords_counts(x):
	l = len([t for t in x.split() if t in stopwords])
	return l

#method for calculating hashtag(#) counts:
def _get_hashtag_counts(x):
	l = len([t for t in x.split() if t.startwith('#')])
	return l

#methd for calculating mention(@) counts:
def _get_mentions_counts(x):
	l = len([t for t in x.split() if t.startwith('')])
	return l

#method for calculating digits count:
def _get_digit_counts(x):
	return len([t for t in x.split() if t.isdigit()])

#method for calculating upper case counts:
def _get_uppercase_counts(x):
	return len([t for t in x.split() if t.isupper()])

#method for contraction words to expansion words:
def _cont_exp(x):
	contractions = { 
	"ain't": "am not",
	"aren't": "are not",
	"can't": "cannot",
	"can't've": "cannot have",
	"'cause": "because",
	"could've": "could have",
	"couldn't": "could not",
	"couldn't've": "could not have",
	"didn't": "did not",
	"doesn't": "does not",
	"don't": "do not",
	"hadn't": "had not",
	"hadn't've": "had not have",
	"hasn't": "has not",
	"haven't": "have not",
	"he'd": "he would",
	"he'd've": "he would have",
	"he'll": "he will",
	"he'll've": "he will have",
	"he's": "he is",
	"how'd": "how did",
	"how'd'y": "how do you",
	"how'll": "how will",
	"how's": "how does",
	"i'd": "i would",
	"i'd've": "i would have",
	"i'll": "i will",
	"i'll've": "i will have",
	"i'm": "i am",
	"i've": "i have",
	"isn't": "is not",
	"it'd": "it would",
	"it'd've": "it would have",
	"it'll": "it will",
	"it'll've": "it will have",
	"it's": "it is",
	"let's": "let us",
	"ma'am": "madam",
	"mayn't": "may not",
	"might've": "might have",
	"mightn't": "might not",
	"mightn't've": "might not have",
	"must've": "must have",
	"mustn't": "must not",
	"mustn't've": "must not have",
	"needn't": "need not",
	"needn't've": "need not have",
	"o'clock": "of the clock",
	"oughtn't": "ought not",
	"oughtn't've": "ought not have",
	"shan't": "shall not",
	"sha'n't": "shall not",
	"shan't've": "shall not have",
	"she'd": "she would",
	"she'd've": "she would have",
	"she'll": "she will",
	"she'll've": "she will have",
	"she's": "she is",
	"should've": "should have",
	"shouldn't": "should not",
	"shouldn't've": "should not have",
	"so've": "so have",
	"so's": "so is",
	"that'd": "that would",
	"that'd've": "that would have",
	"that's": "that is",
	"there'd": "there would",
	"there'd've": "there would have",
	"there's": "there is",
	"they'd": "they would",
	"they'd've": "they would have",
	"they'll": "they will",
	"they'll've": "they will have",
	"they're": "they are",
	"they've": "they have",
	"to've": "to have",
	"wasn't": "was not",
	" u ": " you ",
	" ur ": " your ",
	" n ": " and ",
	"won't": "would not",
	'dis': 'this',
	'bak': 'back',
	'brng': 'bring'}

	if type(x) is str:
		for key in contractions:
			value = contractions[key]
			x = x.replace(key,value)
		return x
	else:
		return x


#count emails:
def _get_emails(x):
	emails = re.findall(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+\b)', x)
	counts = len(emails)

	return counts,emails

#remove emails:
def _remove_emails(x):
	return re.sub(r'([a-z0-9+._-]+@[a-z0-9+._-]+\.[a-z0-9+_-]+)',"", x)

#URL's present:
def _get_urls(x):
	urls = re.findall(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', x)
	counts = len(urls)

	return counts,urls

#remove urls:
def _remove_urls(x):
	return re.sub(r'(http|https|ftp|ssh)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '' , x)

#remove re-tweets:
def _remove_rt(x):
	return re.sub(r'\brt\b', '', x).strip()

#remove special characters:
def _remove_special_chars(x):
	x = re.sub(r'[^\w ]+', "", x)
	x = ' '.join(x.split())
	return x

#remove html tags:
def _remove_html_tags(x):
	return BeautifulSoup(x, 'lxml').get_text().strip()

#remove ascented characters:
def _remove_accented_chars(x):
	x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('utf-8', 'ignore')
	return x

 #remove stopwords
def _remove_stopwords(x):
 	return ' '.join([t for t in x.split() if t not in stopwords])

#lemmatisation
def _make_base(x):
	x = str(x)
	x_list = []
	doc = nlp(x)
	
	for token in doc:
		lemma = token.lemma_
		if lemma == '-PRON-' or lemma == 'be':
			lemma = token.text

		x_list.append(lemma)
	return ' '.join(x_list)

def _get_value_counts(df,col):
	text = ' '.join(df[col])
	text = text.split()
	freq = pd.Series(text).value_counts()
	return freq

#remove commono words:
def _remove_common_words(x,freq,n=20):
	fn = freq[:n]
	x = ' '.join([t for t in x.split() if t not in fn])
	return x

#remove rare words:
def _remove_rarewords(x,freq,n=20):
	fn = freq_common.tail(n)
	x = ' '.join([t for t in x.split() if t not in fn])
	return x

#spelling correction
def _spelling_correction(x):
	x = TextBlob(x).correct()
	return x



