from nltk import word_tokenize, sent_tokenize
import re
from nltk.stem import PorterStemmer


class InputOutputIdentifier:
    outputIndicators = ['then', 'will', 'activate''generate', 'create', 'give', 'turn', 'operate', 'start']
    inputIndicators = ['and', 'if', 'only', 'when', 'either', 'all']

    def __init__(self, entity_set,text):
        self.entity_set = entity_set
        self.text = text
        self.input_set = set()
        self.output_set = set()
        self.neighbour_dic = {}

    def neighbourhood_based_identification(self):
        ps = PorterStemmer()
        sentences = sent_tokenize(self.text)
        for sentence in sentences:
            for entity in self.entity_set:
                # get the surrounded words of a given word
                r1 = re.search(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,2}" + entity + "(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,2}",sentence)
                if r1 is None:
                    continue
                else:
                    print(r1.group())
                    self.neighbour_dic[entity] = word_tokenize(r1.group());

        for entity in self.entity_set:
            neighbours = self.neighbour_dic[entity]
            stem_neighbours = []
            for neighbour in neighbours:
                stem_neighbours.append(ps.stem(neighbour))
            for stem_neighbour in stem_neighbours:
                if stem_neighbour in InputOutputIdentifier.inputIndicators:  # check whether a stem word is inside input indicators
                    self.input_set.add(entity)
                elif stem_neighbour in InputOutputIdentifier.outputIndicators:  # check whether a stem word is inside output indicators
                    self.output_set.add(entity)



