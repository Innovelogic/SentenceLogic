import EntityExtractor,InputOutputIdentifier
from EntityExtractor import *
from InputOutputIdentifier import *
from SentenceFilter import *
from EntityReferencer import *
import re


with open('../data/data2.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '')  # example text is read from data2.txt


def chunk_before_send(text):
    chunks = []
    input_pattern = re.compile(".I[A-Z]=1/0")
    output_pattern = re.compile(".O[A-Z]=1/0")

    sentences = sent_tokenize(text)
    grammar = r"""
          NBAR  : {<NN.*>*<NN.*>}                
          CCAR  : {<CC><NBAR>}     # [and X]
          NCAR  : {<NBAR><CCAR>*}  # Pressure sensor [and X][and Y][and Z]                
          FUTPAS: {<MD><RB>*<VB>}
          NOV   : {<VBZ|VBP><RB>}
          PHR   : {<VBN><IN|RP>} 
          PAS   : {<VBZ|VBP|FUTPAS|NOV><RB>*<VBN|JJ|VBG|PHR>}  
          FUT   : {<MD><RB>*<VB>}
          NOT   : {<VBZ|VBP><RB><VB>} 
          ACT   : {<RB>*<VBZ|VBP|FUT|NOT>}               
          GR    : {<NBAR|NCAR><ACT|PAS>}
          """

    termVerbDic = {}
    for sent in sentences:
        sent_chunks = []
        words = word_tokenize(sent)
        tagged = pos_tag(words)
        cp = RegexpParser(grammar)
        t = cp.parse(tagged)
       # t.draw()
        for s in t.subtrees():
            termVerbs = []
            term = ""
            if s.label() == "GR":
                current_str = ""
                for token in s.leaves():
                    current_str = current_str + " " + token[0]
                    if token[1] == "RB" or token[1] == "VBG"or token[1] == "VBZ"or token[1] == "VBP"or token[1] == "MD" or token[1] == "VB"or token[1] == "VBN"or token[1] == "IN" or token[1] == "JJ" or token[1] == "RP":
                        termVerbs.append(token[0])
                    elif token[1] == "NNP":
                        if term:
                            term = term+","+token[0]
                        else:
                            term = term + token[0]

                termVerbDic[term] = termVerbs
                sent_chunks.append(current_str)
        chunks.append(sent_chunks)
    #print(termVerbDic)
    new_chunks = []
    for chunk in chunks:
        new_sent_chunks = []
        input_chunks = []
        output_chunks = []
        for sent_chunk in chunk:
            if input_pattern.match(sent_chunk):
                input_chunks.append(sent_chunk)
            elif output_pattern.match(sent_chunk):
                output_chunks.append(sent_chunk)

        new_sent_chunks.append(input_chunks)
        new_sent_chunks.append(output_chunks)

        new_chunks.append(new_sent_chunks)

    return new_chunks


def input_output_identification_display(input_output_identifier):
    if input_output_identifier.output_set & input_output_identifier.output_set:
        return conversion_method(sample_sentences, input_output_identifier)
    elif (not input_output_identifier.output_set) & (not input_output_identifier.output_set):
        print("HINT : Both Input and Output Sets are Empty")
        return conversion_method(sample_sentences, input_output_identifier)
        #sys.exit("Error message")
    elif input_output_identifier.input_set:
        print("HINT : Output Set is Empty")
        return conversion_method(sample_sentences, input_output_identifier)
        #sys.exit("Error message")
    else:
        print("HINT : Input Set is Empty")


def conversion_method(sentences,input_output_identifier):

    print("Example :", example_sentence)
    print("Inputs :", input_output_identifier.input_set)
    print("Outputs :", input_output_identifier.output_set)


    x = ord('A')
    for input in input_output_identifier.input_set:
        input_output_dic['I' + chr(x)] = input
        x = x + 1

    x = ord('Z')
    for output in input_output_identifier.output_set:
        input_output_dic['O' + chr(x)] = output
        x = x - 1

    conversion = sentences
    for word in input_output_dic:
        conversion = conversion.replace(" "+input_output_dic[word]+" ", " "+word+"=1/0 ")

    print(conversion)
    return conversion


def method_one():

    print("====================================NER based Extraction Approach============================================")
    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_with_ner()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    tagged = input_output_identification_display(input_output_identifier)
    #new_taggings = chunk_before_send(tagged)
    print(
        "=============================================================================================================\n")




def method_two():
    print("===========================Regex based normal Extraction Approach============================================")

    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_with_regex()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    tagged = input_output_identification_display(input_output_identifier)
    #new_taggings = chunk_before_send(tagged)
    print(
        "=============================================================================================================\n")




def method_three():


    print("========================Regex based Verb analysed Extraction Approach========================================")

    # Create Entity Extractor Object
    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_verb_based()
    print(entity_extractor.entitySet)

    print(sample_sentences)
    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    tagged = input_output_identification_display(input_output_identifier)

    inputs = len(input_output_identifier.input_set)
    outputs = len(input_output_identifier.output_set)

    print("=============================================================================================================\n")

    return [tagged,inputs,outputs]


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
ref_dic = entity_referencer.refer_entities()
print(ref_dic)

# Replace logic sentences with references
sample_sentences = " ".join(sentence for sentence in sentence_filter.logic_sentences)
for word in entity_referencer.referencing_Dic:
    sample_sentences = sample_sentences.replace(word, entity_referencer.referencing_Dic[word])

# Identify the IO status
if sentence_filter.description_sentences:
    io_pattern = re.compile("(I/O_Status:).")
    for sent in sentence_filter.description_sentences:
        if io_pattern.match(sent):
            input_output_status_sentences = sent.split("I/O_Status: ",1)[1]
            #print(input_output_status_sentences)

else:
    print("HINT :Please Enter the descriptions about the problem")
    #sys.exit("Error message")

# Start the process
input_output_dic = {}
method_one()
method_two()
tagged = method_three()
new_taggings = chunk_before_send(tagged[0])

# Things are to be shared with next module
print("==================================Things are to be shared with next module==================================")
print("IO_Status : ",input_output_status_sentences.replace(",", "."))
print("Tagged Setences : ",tagged[0])
print("Tag Dictionary : ",input_output_dic)
print("Number of Inputs : ",tagged[1])
print("Number of Outputs : ",tagged[2])
print("Tag Dictionary : ",input_output_dic)
print("Reference Dictionary : ",entity_referencer.referencing_Dic)
print("New Chunk List : ",new_taggings)


print("============================================================================================================")
