# from sklearn import tree
# features = [[140,1],[130,1],[150,0],[170,0]]
# labels = [0,0,1,1]
# clf = tree.DecisionTreeClassifier();
# clf = clf.fit(features, labels)
# print (clf.predict([[140,0]]))

from collections import Counter

import nltk
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize



#=================Text data aquisition process===============================
with open('data.txt', 'r') as myfile:
    example_sentence=myfile.read().replace('\n', '')

#stop_words = set(stopwords.words("english"))
# expressions =re.findall(r'[A-Z]=[0-1]*;',example_sentence)
# print(expressions)
values = re.findall(r'=\d{1}',example_sentence)
labels = re.findall(r'[A-Z]=',example_sentence)
index = 0
dataList = []
for eachvalue in values:
    dataDic = {}
    dataDic[labels[index][0]] = eachvalue[1]
    index += 1
    dataList.append(dataDic)

print(dataList)







