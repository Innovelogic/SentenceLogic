from nltk import word_tokenize, sent_tokenize, pos_tag, RegexpParser,ne_chunk,Tree


class EntityExtractor:

    def __init__(self, text):
        self.text = text
        self.entitySet = set()

    # Extracting entities using named entity recognition
    def extraction_with_ner(self):
        print(pos_tag(word_tokenize(self.text)))
        chunked = ne_chunk(pos_tag(word_tokenize(self.text)), binary = True)
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            # print(i)
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue
        self.entitySet = set(continuous_chunk)

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
            for tree in chunk.subtrees(filter=lambda t: t.label() == 'NP'):
                self.entitySet.add(' '.join([child[0] for child in tree.leaves()]))

    # Extracting entities using verb based approach
    def extraction_verb_based(self):

        sentences = sent_tokenize(self.text)
        grammar = r"""
              NBAR  : {<NN.*>*<NN.*>}                
              CCAR  : {<CC><NBAR>}     # [and X]
              NCAR  : {<NBAR><CCAR>*}  # Pressure sensor [and X][and Y][and Z]                
              FUTPAS: {<MD><RB>*<VB>}
              NOV   : {<VBZ|VBP><RB>}
              PAS   : {<VBZ|VBP|FUTPAS|NOV><RB>*<VBN|JJ|VBG>}
              NOT   : {<VBZ|VBP><RB><VB>} 
              ACT   : {<RB>*<VBZ|VBP|FUTPAS|NOT>}               
              GR    : {<NBAR|NCAR><ACT|PAS>}
              """

        for sent in sentences:
            words = word_tokenize(sent)
            tagged = pos_tag(words)
            cp = RegexpParser(grammar)
            t = cp.parse(tagged)
            t.draw()
            for s in t.subtrees():
                if s.label() == "GR":
                    current_str = ""
                    for token in s.leaves():
                        if token[1] == "NNS" or token[1] == "VBZ" or token[1] == "VBP" or token[1] == "NOV" or token[1] == "MD" or token[1] == "RB":
                            break
                        elif token[1] == "CC":
                            self.entitySet.add(current_str)
                            current_str = ""
                            continue
                        else:
                            if current_str == "":
                                current_str = current_str + token[0]
                            else:
                                current_str = current_str + " "+token[0]
                    if current_str != "":
                        self.entitySet.add(current_str)






