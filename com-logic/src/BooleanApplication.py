import EntityExtractor,InputOutputIdentifier
from EntityExtractor import *
from InputOutputIdentifier import *


def main():

    with open('../data/data2.txt', 'r') as myfile:
        example_sentence = myfile.read().replace('\n', '')  # example text is read from data2.txt
    entity_extractor = EntityExtractor(example_sentence)
    entity_extractor.extraction_with_regex()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,example_sentence)
    input_output_identifier.neighbourhood_based_identification()

    print("Example :",example_sentence)
    print("Inputs :",input_output_identifier.input_set)
    print("Outputs :",input_output_identifier.output_set)

main()
