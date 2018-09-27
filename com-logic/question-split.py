import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

# =================Text data aquisition process===============================
with open('data.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '')

questions_all = example_sentence.split("Q.")
print(questions_all)
print(len(questions_all))

res = []


def pos_addition(sents):
    try:
        for i in sents:
            words = word_tokenize(i)
            filtered_sentence = []
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)
            tagged = nltk.pos_tag(filtered_sentence)
            chunk_gram = r"""Chunk:{<NN>$}"""
            chunk_parser = nltk.RegexpParser(chunk_gram)
            chunked_data = chunk_parser.parse(tagged)
            # print(chunked_data)
            # chunked_data.draw();

    except Exception as e:
        print(str(e))


def ne_addition(sents):
    # sents = nltk.sent_tokenize(problem)

    try:
        #     for i in sents:
        #         words = word_tokenize(i)
        #         filtered_sentence = []
        #         # for w in words:
        #         #     if w not in stop_words:
        #         #         filtered_sentence.append(w)
        #         tagged = nltk.pos_tag(words)
        #         res.append(tagged)
        #         # print(tagged)
        return (nltk.pos_tag(word_tokenize(sents)))

    except Exception as e:
        print(str(e))


def single_quantifier(res):
    Comma_count = 0
    CC_count = 0
    CD_count = 0
    Dot_count = 0
    DT_count = 0
    EX_count = 0
    IN_count = 0
    JJ_count = 0
    JJR_count = 0
    MD_count = 0
    NNP_count = 0
    NN_count = 0
    NNS_count = 0
    RB_count = 0
    TO_count = 0
    VBN_count = 0
    VB_count = 0
    VBD_count = 0
    VBP_count = 0
    VBG_count = 0
    VBZ_count = 0
    WDT_count = 0
    WRB_count = 0
    others = 0
    for pair in res:
        tag = pair[1]
        if tag == ',':
            JJ_count += 1
        elif tag == 'CC':
            DT_count += 1
        elif tag == 'CD':
            VBD_count += 1
        elif tag == '.':
            NNS_count += 1
        elif tag == 'DT':
            VBP_count += 1
        elif tag == 'EX':
            NNP_count += 1
        elif tag == 'IN':
            CD_count += 1
        elif tag == 'JJ':
            NN_count += 1
        elif tag == 'JJR':
            DT_count += 1
        elif tag == 'MD':
            VBD_count += 1
        elif tag == 'NNS':
            NNS_count += 1
        elif tag == 'NN':
            VBP_count += 1
        elif tag == 'NNP':
            NNP_count += 1
        elif tag == 'RB':
            CD_count += 1
        elif tag == 'TO':
            NN_count += 1
        elif tag == 'VBN':
            Dot_count += 1
        elif tag == 'VB':
            Comma_count += 1
        elif tag == 'VBD':
            CD_count += 1
        elif tag == 'VBP':
            NN_count += 1
        elif tag == 'VBG':
            DT_count += 1
        elif tag == 'VBZ':
            VBD_count += 1
        elif tag == 'WDT':
            NNS_count += 1
        elif tag == 'WRB':
            VBP_count += 1
        else:
            others += 1
    # print(JJ_count)
    # print(DT_count)
    # print(VBD_count)
    # print(NNS_count)
    # print(VBP_count)
    # print(NNP_count)
    # print(CD_count)
    # print(NN_count)
    # print(Dot_count)
    # print(Comma_count)
    df = pd.DataFrame([[Comma_count, CC_count, CD_count, Dot_count, DT_count, EX_count, IN_count, JJ_count,
                        JJR_count, MD_count, NNS_count, NNP_count, NN_count, NNS_count, RB_count, TO_count,
                        VBN_count, VB_count, VBD_count, VBP_count, VBG_count, VBZ_count, WDT_count, WRB_count,
                        others]],
                      columns=list(['Comma', 'CC', 'CD', 'Dot', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'MD', 'NNS',
                                    'NNP', 'NN', 'NNS', 'RB', 'TO', 'VBN', 'VB', 'VBD', 'VBP', 'VBG', 'VBZ',
                                    'WDT', 'WRB', 'others']))
    return df


df = pd.DataFrame(columns=list(
        ['Comma', 'CC', 'CD', 'Dot', 'DT', 'EX', 'IN', 'JJ', 'JJR', 'MD', 'NNS',
         'NNP', 'NN', 'NNS', 'RB', 'TO', 'VBN', 'VB', 'VBD', 'VBP', 'VBG', 'VBZ',
         'WDT', 'WRB', 'others']))

for i in questions_all:
    # print(i)
    # print("\n")
    # print("this is i", i)
    res = ne_addition(i)
    # print(res)
    df2 = single_quantifier(res)
    print("this is df2", df2)
    # for i in range(number_of_questions):
    # print(df)
    df = df.append(df2, ignore_index=True)

print(df)
# =================Text data aquisition process===============================
# with open('data.txt', 'r') as myfile:
#     example_sentence = myfile.read().replace('\n', '')

# ===============Stop Words in English ===============================
stop_words = set(stopwords.words("english"))

# ==================Tokenize the sentences============================

# sents = sent_tokenize(example_sentence)
# print(sents)
# ========================NE Recognition==================================


#
# print(res)


# ====================POS Tagging only=================================


# ====================Stemming=================================
'''
    from nltk.stem import PorterStemmer

    from nltk.tokenize import word_tokenize

    ps = PorterStemmer();

    example_words = ["python","pythoning","pythoner","pythoned","pythonly"]




    for w in example_words:
        print(ps.stem(w))
'''
# =============================================================

# ===================== classification ========================
import xgboost as xgb
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

kmean = KMeans (n_clusters=8, random_state=0).fit(df)
print(kmean.labels_)

