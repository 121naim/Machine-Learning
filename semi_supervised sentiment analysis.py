import collections

import random
import re
from collections import Counter
from itertools import islice
import nltk
from nltk.corpus import stopwords
import numpy as np 
import pandas as pd 
pd.set_option('display.max_colwidth', -1)
from time import time
import re
import string
import os
import emoji
from pprint import pprint
import collections
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
sns.set(font_scale=1.3)
from sklearn.metrics import f1_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import gensim
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings('ignore')
np.random.seed(37)  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder                           
                           
arabic_diacritics = re.compile(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', str(text))
    return text



def remove_repeating_char(text):
    # return re.sub(r'(.)\1+', r'\1', text)     # keep only 1 repeat
    return re.sub(r'(.)\1+', r'\1\1', text)  # keep 2 repeat

def process_text(text, grams=False):
    clean_text = remove_diacritics(text)
    clean_text = remove_repeating_char(clean_text)
    
    if grams is False:
        return nltk.tokenize.sent_tokenize(clean_text)
    else:
        tokens = nltk.tokenize.sent_tokenize(clean_text)
        grams = list(window(tokens))
        grams = [' '.join(g) for g in grams]
        grams = grams + tokens
        return grams


def window(words_seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(words_seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result
def document_features(document, corpus_features):
    document_words = set(document)
    features = {}
    for word in corpus_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features


all_features = list()
texts = list()
data_labels = list()
import pyarabic.arabrepr
arepr = pyarabic.arabrepr.ArabicRepr()
repr = arepr.repr
from tashaphyne.stemming import ArabicLightStemmer
ArListem = ArabicLightStemmer()

negative_file = open("C:/Users/121/.spyder-py3/text_mining/negative_tweets.txt", encoding ="utf8")
positive_file = open("C:/Users/121/.spyder-py3/text_mining/positive_tweets.txt", encoding ="utf8")

n_grams_flag = False
min_freq = 13

print('read data ...')
print('read data ...')
# read positive data
for line in positive_file:
    
    text_features = process_text(line, grams=n_grams_flag)
    stop_words = set(stopwords.words('arabic'))
    text_features = [w for w in text_features if not w in stop_words]
    all_features += text_features
    texts.append(text_features)
    data_labels.append('pos')   


for line in negative_file:
    
    text_features = process_text(line, grams=n_grams_flag)
    stop_words = set(stopwords.words('arabic'))
    text_features = [w for w in text_features if not w in stop_words]
    all_features += text_features
    texts.append(text_features)
    data_labels.append('neg')
   
df = pd.DataFrame(list(zip(texts, data_labels)),
              columns=['texts','data_labels'])

"""
df1 = df.iloc[6000:9000, : ]

df.to_excel ('C:/Users/121/.spyder-py3/text_mining/train.xlsx', index = False, header=True,encoding="utf-8-sig")
df1.to_excel ('C:/Users/121/.spyder-py3/text_mining/test.xlsx', index = False, header=True,encoding="utf-8-sig")

train = pd.read_excel('C:/Users/121/.spyder-py3/text_mining/train.xlsx' , encoding = "utf8")
test = pd.read_excel('C:/Users/121/.spyder-py3/text_mining/train.xlsx',encoding = "utf8")
#trainig 


training = train 
testing = test 
y_train = training['data_labels'] 
training.drop('data_labels',axis=1,inplace=True)
features = training.columns
target = 'data_labels'


X_train, X_test = training, testing

import imblearn
!pip install imblearn
from imblearn.over_sampling import SMOTE

sm = SMOTE()

X_train_res, y_train_res = sm.fit_sample(X_train_vect, y_train)
"""

X_train, X_test, y_train, y_test= train_test_split(df, data_labels, test_size=0.2, random_state=42)
from sklearn.feature_extraction.text import CountVectorizer

vect = CountVectorizer(max_features=1000, binary=True)

X_train_vect = vect.fit_transform(X_train)

import imblearn
#!pip install imblearn
from imblearn.over_sampling import SMOTE

sm = SMOTE()

X_train_res, y_train_res = sm.fit_sample(X_train_vect, y_train)

from sklearn.naive_bayes import MultinomialNB

nb = MultinomialNB()

nb.fit(X_train_res, y_train_res)

nb.score(X_train_res, y_train_res)

