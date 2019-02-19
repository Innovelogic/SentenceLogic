import EntityExtractor,InputOutputIdentifier
from EntityExtractor import *
from InputOutputIdentifier import *
from SentenceFilter import *
from EntityReferencer import *

with open('../data/data2.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '')  # example text is read from data2.txt


def entity_extraction_accuracy_measure():
    return 0


def input_output_identification_accuracy_measure():
    return 0


def conversion_method(sentences,input_output_identifier):

    print("Example :", example_sentence)
    print("Inputs :", input_output_identifier.input_set)
    print("Outputs :", input_output_identifier.output_set)

    input_output_dic = {}
    x = ord('A')
    for input in input_output_identifier.input_set:
        input_output_dic['I' + chr(x)] = input
        x = x + 1

    x = ord('Z')
    for output in input_output_identifier.output_set:
        input_output_dic['O' + chr(x)] = output
        x = x - 1
    print(input_output_dic)
    conversion = sentences
    for word in input_output_dic:
        conversion = conversion.replace(input_output_dic[word], input_output_dic[word]+" [" + word+"]")

    print(conversion)


def method_two():
    print("===========================Regex based normal Extraction Approach============================================")

    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_with_regex()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    conversion_method(sample_sentences, input_output_identifier)

    print("=============================================================================================================\n")


def method_three():


    print("========================Regex based Verb analysed Extraction Approach========================================")

    # Create Entity Extractor Object
    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_verb_based()
    print(entity_extractor.entitySet)

    print(sample_sentences)
    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    conversion_method(sample_sentences,input_output_identifier)
    print("=============================================================================================================\n")


def method_one():

    print("====================================NER based Extraction Approach============================================")
    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_with_ner()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    conversion_method(sample_sentences,input_output_identifier)
    print("=============================================================================================================")


# Create sentence filter object
sentence_filter = SentenceFilter(example_sentence)

# Filtering sentences for description sentences and to logic sentences
sentence_filter.filter_sentences()

if sentence_filter.description_sentences:
    # Create referencer object
    entity_referencer = EntityReferencer(sentence_filter.description_sentences)
else:
    # Create referencer object
    entity_referencer = EntityReferencer(sentence_filter.logic_sentences)

# Refer entities
entity_referencer.refer_entities()

# Replace logic sentences with references
sample_sentences = " ".join(sentence for sentence in sentence_filter.logic_sentences)
for word in entity_referencer.referencing_Dic:
    sample_sentences = sample_sentences.replace(word, entity_referencer.referencing_Dic[word])



# Start the process
method_one()
method_two()
method_three()
