import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
with open('data/data2.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '')


def pos_addition(filtered_sentences):
    try:
        filtered_conjunctions = []

        for i in filtered_sentences:
            words = word_tokenize(i)
            filtered_sentence = []
            filtered_conjunctions = []
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)
                else:
                    filtered_conjunctions.append(w)
            tagged = nltk.pos_tag(filtered_sentence)
            print(tagged)
        print("Stop words in the text : ", str(filtered_conjunctions))
    except Exception as e:
        print(str(e))


def extract_nn(sent):
    grammar = r"""
    NBAR:
        {<NN.*>*<NN.*>}
    NP:
        {<NBAR>}
        {<NBAR><IN><NBAR>}
    """

    chunker = nltk.RegexpParser(grammar)
    ne = set()
    chunk = chunker.parse(nltk.pos_tag(nltk.word_tokenize(sent)))
    chunk.draw()
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne


stop_words = set(stopwords.words("english"))
sentences = sent_tokenize(example_sentence)
print('Sample problem :' + str(example_sentence))
pos_addition(sentences)
entity_set = extract_nn(example_sentence)
print('Entity Set:' + str(entity_set))

