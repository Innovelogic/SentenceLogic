import nltk
from nltk import sent_tokenize, word_tokenize,pos_tag,RegexpParser
exmple = 'A dog has sharp teeth so that it can eat flesh very easily. It has four legs, two ears, two eyes, a tail, a mouth, and a nose. It is very clever domestic animal and has been proved very useful in catching thieves and criminals. It does so as it has very powerful sense of hearing and smelling.'

sentences = sent_tokenize(exmple)

for i in sentences:
    words = word_tokenize(i)
    tagged = pos_tag(words)

    chunkGram = r"""Chunk:{<RB.?><VB.?>*<NNP><NN>?}"""
    chunkParser = RegexpParser(chunkGram)
    chunk = chunkParser.parse(tagged)
    chunk.draw()