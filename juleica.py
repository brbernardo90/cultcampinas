from re import compile
from itertools import chain
from collections import Counter, namedtuple
# from reverend.thomas import Bayes
import requests
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import cross_val_score


urlApi = 'http://www.cultcampinas.com.br/api/all'

headers = {'content-type': 'application/json'}

resposta = requests.get(urlApi, headers=headers)

content = json.loads(resposta._content.decode('UTF-8'))

rows = [([x["tag"], x["desc"]]) for x in content]

df_train = pd.DataFrame(rows, columns=['tag', 'desc'])

vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(df_train['desc'].values)

tf_transformer = TfidfTransformer(use_idf=False).fit(counts)
counts = tf_transformer.transform(counts)

classifier = MultinomialNB(alpha=10)
targets = df_train['tag'].values
classifier.fit(counts, targets)

d = cross_val_score(classifier, counts, targets, cv=5, scoring='log_loss')

print(d.mean())


