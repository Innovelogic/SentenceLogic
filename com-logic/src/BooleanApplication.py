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

    term_verb_dic = {}
    input_pattern1 = re.compile('I[A-Z]=1/0')
    output_pattern2 = re.compile('O[A-Z]=1/0')
    for sent in sentences:
        sents = sent.split(',')

        if len(sents)!=2:
            return print("Please enter the conditions according to the correct format with commas.")

        else:
            input_count1 = len(input_pattern1.findall(sents[0]))
            output_count1 = len(output_pattern2.findall(sents[0]))
            input_count2 = len(input_pattern1.findall(sents[1]))
            output_count2 = len(output_pattern2.findall(sents[1]))
            first = [input_count1,output_count1]
            second = [input_count2,output_count2]
            sent_chunks = []
            words = word_tokenize(sent)
            tagged = pos_tag(words)
            cp = RegexpParser(grammar)
            t = cp.parse(tagged)
            t.draw()
            for s in t.subtrees():
                term_verbs = []
                term = ""
                if s.label() == "GR":
                    current_str = ""
                    for token in s.leaves():
                        current_str = current_str + " " + token[0]
                        if token[1] == "RB" or token[1] == "VBG"or token[1] == "VBZ"or token[1] == "VBP"or token[1] == "MD" or\
                                token[1] == "VB"or token[1] == "VBN"or token[1] == "IN" or token[1] == "JJ" or token[1] == "RP":
                            term_verbs.append(token[0])
                        elif token[1] == "NNP":
                            if term:
                                term = term+","+token[0]
                            else:
                                term = term + token[0]

                    term_verb_dic[term] = term_verbs
                    sent_chunks.append(current_str)
            chunks.append([sent_chunks,first,second])

        # print(termVerbDic)
        new_chunks = []
        n=0
        for chunk in chunks:
            new_sent_chunks = []
            input_chunks = []
            output_chunks = []

            for sent_chunk in chunk[0]:
                if input_pattern.match(sent_chunk):
                    input_chunks.append(sent_chunk)
                elif output_pattern.match(sent_chunk):
                    output_chunks.append(sent_chunk)
            #print(chunk[1][0],chunk[1][1])
            if(not input_chunks) | (not output_chunks):

                print("HINT: Please change the representation of '",sentence_filter.logic_sentences[n],"'" )
            else:
                if(chunk[1][0] is not 0):
                    new_sent_chunks.append(input_chunks)
                    new_sent_chunks.append(output_chunks)
                else:
                    new_sent_chunks.append(output_chunks)
                    new_sent_chunks.append(input_chunks)

            n = n+1
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

    input_output_dic = {}

    x = ord('A')
    for input in input_output_identifier.input_set:
        input_output_dic['I' + chr(x)] = input
        x = x + 1

    x = ord('Z')
    for output in input_output_identifier.output_set:
        input_output_dic['O' + chr(x)] = output
        x = x - 1

    conversion = sentences
    for index in input_output_dic:
        conversion = conversion.replace(" "+input_output_dic[index]+" ", " "+index+"=1/0 ")

    print(conversion,"Print Conversion")
    return [conversion,input_output_dic]


def method_one():

    print("====================================NER based Extraction Approach============================================")
    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_with_ner()
    print(entity_extractor.entitySet)

    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    input_output_identification_display(input_output_identifier)
    #new_taggings = chunk_before_send(tagged)
    print(
        "=============================================================================================================\n")




def method_two():
    print("===========================Regex based normal Extraction Approach============================================")

    entity_extractor1 = EntityExtractor(sample_sentences)
    entity_extractor1.extraction_with_regex()
    print(entity_extractor1.entitySet)

    input_output_identifier1 = InputOutputIdentifier(entity_extractor1.entitySet,sample_sentences)
    input_output_identifier1.neighbourhood_based_identification()

    input_output_identification_display(input_output_identifier1)
    #new_taggings = chunk_before_send(tagged)
    print(
        "=============================================================================================================\n")


def method_three():

    print("========================Regex based Verb analysed Extraction Approach========================================")

    # Create Entity Extractor Object
    entity_extractor2 = EntityExtractor(sample_sentences)
    entity_extractor2.extraction_verb_based()
    print(entity_extractor2.entitySet)

    print(sample_sentences)
    input_output_identifier2 = InputOutputIdentifier(entity_extractor2.entitySet,sample_sentences)
    input_output_identifier2.neighbourhood_based_identification()

    tagged_text = input_output_identification_display(input_output_identifier2)

    inputs = len(input_output_identifier2.input_set)
    outputs = len(input_output_identifier2.output_set)

    print("=============================================================================================================\n")

    return [tagged_text,inputs,outputs]


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
# if sentence_filter.description_sentences:
#     io_pattern = re.compile("^(I/O_Status:)")
#     for sent in sentence_filter.description_sentences:
#         if io_pattern.match(sent):
#             input_output_status_sentences = sent.split("I/O_Status:",1)[1]
#         else :
#             input_output_status_sentences = ''
#
#
# else:
#     print("HINT :Please Enter the descriptions about the problem")
#     #sys.exit("Error message")
with open('../data/io_status.txt', 'r') as io_file:
    input_output_status_sentences = io_file.read().replace('\n', ' ')


# Start the process
method_one()
method_two()

tagged = method_three()
new_taggings = chunk_before_send(tagged[0][0])

# Things are to be shared with next module
print("==================================Things are to be shared with next module==================================")
print("I/O_Status:",input_output_status_sentences.replace(",", "."))
print("Tagged Sentences : ",tagged[0][0])
print("Tag Dictionary : ",tagged[0][1])
print("Number of Inputs : ",tagged[1])
print("Number of Outputs : ",tagged[2])
print("Reference Dictionary : ",entity_referencer.referencing_Dic)
print("New Chunk List : ",new_taggings)


print("============================================================================================================")
