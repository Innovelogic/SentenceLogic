from nltk import word_tokenize, sent_tokenize, pos_tag, ne_chunk, RegexpParser
import re


class EntityExtractor:

    def __init__(self,text):

        self.text = text
        self.entitySet = set()

    # Extracting entities using named entity recognition
    def extraction_with_ner(self):

        sentences = sent_tokenize(self.text)
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]
        ne_chunked_sentences = ne_chunk(tagged_sentences)

        for tagged_tree in ne_chunked_sentences:
            if hasattr(tagged_tree, 'label'):
                entity_name = ' '.join(c[0] for c in tagged_tree.leaves())  #
                entity_type = tagged_tree.label()  # get NE category
                self.entitySet.add(entity_name)

    # Extracting entities using regular expression and POS tagging
    def extraction_with_regex(self):

        grammar = r"""
        NBAR:
            {<NN.*>*<NN.*>}
        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}
        """

        sentences = sent_tokenize(self.text)
        chunker = RegexpParser(grammar)

        for sentence in sentences:
            chunk = chunker.parse(pos_tag(word_tokenize(sentence)))
            print(pos_tag(word_tokenize(self.text)))
            for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
                self.entitySet.add(' '.join([child[0] for child in tree.leaves()]))

    # Extracting entities using verb based approach
    def extraction_verb_based(self):

        sentences = sent_tokenize(self.text)
        pos_tagged = []
        neighbour_dic = {}
        for sent in sentences:
            words = word_tokenize(sent)
            tagged = pos_tag(words)
            grammar = "VERB: {<VB[N|Z]>}"
            cp = RegexpParser(grammar)
            t = cp.parse(tagged)
            t.draw()
            for s in t.subtrees():
                if s.label() == "VERB":
                    if s is not []:
                        verb_part = s.pop()[0]
                        print(verb_part)
                        r1 = re.search(
                            r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,2}" + verb_part + "(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,2}", sent)
                        if r1 is None:
                            continue
                        else:
                            print(r1.group())
                            neighbour_dic[verb_part] = word_tokenize(r1.group());

        print(neighbour_dic)


