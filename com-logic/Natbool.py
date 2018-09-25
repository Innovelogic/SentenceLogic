
import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize



#=================Text data aquisition process===============================
with open('data.txt', 'r') as myfile:
    example_sentence=myfile.read().replace('\n', '')

#===============Stop Words in English ===============================
stop_words = set(stopwords.words("english"))

#==================Tokenize the sentences============================

sents = sent_tokenize(example_sentence)
print(sents)
#========================NE Recognition==================================
res = []
def ne_addition(sents):
    try:
        for i in sents:
            words = word_tokenize(i)
            filtered_sentence = []
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)
            tagged = nltk.pos_tag(filtered_sentence)
            res.append(tagged)
            print(tagged)
            namedEnt = nltk.ne_chunk(tagged)
            #namedEnt.draw()


        # csvfile = "F:\csvmy.csv"
        #
        # # Assuming res is a flat list
        # with open(csvfile, "w") as output:
        #     writer = csv.writer(output, lineterminator='\n')
        #     for val in res:
        #         writer.writerow([val])
        #
        #         # Assuming res is a list of lists
        # with open(csvfile, "w") as output:
        #     writer = csv.writer(output, lineterminator='\n')
        #     writer.writerows(res)
    except Exception as e:
        print(str(e))

ne_addition(sents)


#====================POS Tagging only=================================

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
            print(chunked_data)
            #chunked_data.draw();



    except Exception as e:
        print(str(e))

pos_addition(sents)



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



