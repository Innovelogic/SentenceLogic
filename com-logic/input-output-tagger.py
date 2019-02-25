import nltk
import  re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer

with open('data/data2.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '') # example text is read from data2.txt


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
    print(nltk.pos_tag(nltk.word_tokenize(sent)))
    for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
        ne.add(' '.join([child[0] for child in tree.leaves()]))
    return ne

stop_words = set(stopwords.words("english"))
sentences = sent_tokenize(example_sentence)
ps = PorterStemmer() # Stemmer declaration

print('Sample problem :' + str(example_sentence))

entity_set = extract_nn(example_sentence)
print('Entity Set:' + str(entity_set))

outputIndicators = ['then','will','activate''generate','create','give','turn','operate','start','result']
inputIndicators = ['and','if','only','when','either','all']

neighbourDic = {}  # neighbours dictionary (word->[neighbours])
inputSet = set()    # set ot inputs
outputSet = set()  # set ot inputs

for sentence in sentences:
    for entity in entity_set:
        r1 = re.search(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,2}"+entity+"(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,2}",sentence)  # get the surrounded words of a given word
        if(r1 is None):
            continue
        else:
            print(r1.group())
            neighbourDic[entity]=word_tokenize(r1.group());

# presenceAbsence = {}
# for entity in entity_set:
#     neighbs =neighbourDic[entity]
#     stemNeigbs =[]
#     for neigbh in neighbs:
#         stemNeigbs.append(ps.stem(neigbh))
#     temporaryList = []
#     for feature in features:
#         if(feature in stemNeigbs):
#             temporaryList.append(1)
#         else:
#             temporaryList.append(0)
#     presenceAbsence[entity]=temporaryList

# print(presenceAbsence)


for entity in entity_set:
    neighbs =neighbourDic[entity]
    stemNeigbs =[]
    for neigbh in neighbs:
        stemNeigbs.append(ps.stem(neigbh))
    for stemWord in stemNeigbs:
        if(stemWord in inputIndicators): # check whether a stemword is inside input indicators
            inputSet.add(entity)
        elif(stemWord in outputIndicators): # check whether a stemword is inside output indicators
            outputSet.add(entity)

print("Inputs :",inputSet)
print("Outputs :",outputSet)

