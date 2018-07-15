# ======================Tokenizing=========================
# from nltk.tokenize \
#     import sent_tokenize,word_tokenize
#
# example_text = "Hello there, how are you doing today? The weather is great and Pythom is awesome.The sky is blue. Do not eat card board"
#
# print(sent_tokenize(example_text))
# print(word_tokenize(example_text))

#===============Stop Words=================================

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

example_sentence = "If the door is opened then the blub is switched-off"
stop_words = set(stopwords.words("english"))

words = word_tokenize(example_sentence)
filtered_sentence = []
for w in words:
    if w not in stop_words:
        filtered_sentence.append(w)

print(filtered_sentence)



#====================Stemming=================================
'''
    from nltk.stem import PorterStemmer

    from nltk.tokenize import word_tokenize

    ps = PorterStemmer();

    example_words = ["python","pythoning","pythoner","pythoned","pythonly"]

    for w in example_words:
        print(ps.stem(w))
'''
#=============================================================


