# import nltk
# from nltk import sent_tokenize, word_tokenize,pos_tag,RegexpParser
# exmple = 'A dog has sharp teeth so that it can eat flesh very easily. It has four legs, two ears, two eyes, a tail, a mouth, and a nose. It is very clever domestic animal and has been proved very useful in catching thieves and criminals. It does so as it has very powerful sense of hearing and smelling.'
#
# sentences = sent_tokenize(exmple)
#
# for i in sentences:
#     words = word_tokenize(i)
#     tagged = pos_tag(words)

#     chunkGram = r"""Chunk:{<RB.?><VB.?>*<NNP><NN>?}"""
#     chunkParser = RegexpParser(chunkGram)
#     chunk = chunkParser.parse(tagged)
#     chunk.draw()


# import spacy
# # Load the large English NLP model
# nlp = spacy.load('en_core_web_lg')
#
# # The text we want to examine
# text = """A vehicle with two doors, door X and door Y has a light to show whether the two doors are properly closed. When one or both doors are open, the light will be switched on, When both doors are closed, the light will switched off.
# """
#
# # Parse the text with spaCy. This runs the entire pipeline.
# doc = nlp(text)
#
# # 'doc' now contains a parsed version of text. We can use it to do anything we want!
# # For example, this will print out all the named entities that were detected:
# for entity in doc.ents:
#     print(f"{entity.text} ({entity.label_})")


# import spacy
# import textacy.extract
#
# # Load the large English NLP model
# nlp = spacy.load('en_core_web_lg')
#
# # The text we want to examine
# text = """A vehicle with two doors door X and door Y. Also it has a light to show whether the two doors are properly closed. When one or both doors are open, the light will be switched on, When both doors are closed, the light will switched off.
# """
#
# # Parse the document with spaCy
# doc = nlp(text)
#
# # Extract semi-structured statements
# statements = textacy.extract.semistructured_statements(doc, "door X")
#
# # Print the results
# print("Here are the things I know about London:")
#
# for statement in statements:
#     subject, verb, fact = statement
#     print(f" - {fact}")

#
# from pycorenlp import StanfordCoreNLP
#
# nlp = StanfordCoreNLP('http://localhost:9000')
#
#
# def resolve(corenlp_output):
#     """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
#     for coref in corenlp_output['corefs']:
#         mentions = corenlp_output['corefs'][coref]
#         antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
#         for j in range(1, len(mentions)):
#             mention = mentions[j]
#             if mention['type'] == 'PRONOMINAL':
#                 # get the attributes of the target mention in the corresponding sentence
#                 target_sentence = mention['sentNum']
#                 target_token = mention['startIndex']-1
#                 # transfer the antecedent's word form to the appropriate token in the sentence
#                 corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']
#
#
# def print_resolved(corenlp_output):
#     """ Print the "resolved" output """
#     possessives = ['hers', 'his', 'their', 'theirs','its']
#     for sentence in corenlp_output['sentences']:
#         for token in sentence['tokens']:
#             output_word = token['word']
#             # check lemmas as well as tags for possessive pronouns in case of tagging errors
#             if token['lemma'] in possessives or token['pos'] == 'PRP$':
#                 output_word += "'s"  # add the possessive morpheme
#             output_word += token['after']
#             print(output_word, end='')
#
#
# text = "A vehicle with two doors, door X and door Y has a light to show whether the two doors are properly closed." \
#        "When one or both doors are open, the light will be switched on, When both doors are closed, the light will switched off."
#
# output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})
#
# resolve(output)
#
# print('Original:', text)
# print('Resolved: ', end='')
# print_resolved(output)




# from nltk.tree import Tree
#
# def get_continuous_chunks(text):
#     chunked = ne_chunk(pos_tag(word_tokenize(text)))
#     continuous_chunk = []
#     current_chunk = []
#     for i in chunked:
#         if type(i) == Tree:
#             current_chunk.append(" ".join([token for token, pos in i.leaves()]))
#         elif current_chunk:
#             named_entity = " ".join(current_chunk)
#             if named_entity not in continuous_chunk:
#                 continuous_chunk.append(named_entity)
#                 current_chunk = []
#         else:
#             continue
#
#     return continuous_chunk
#
# my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."
# print(get_continuous_chunks(my_sent))

# from nltk import ne_chunk, pos_tag, word_tokenize
# tokens = word_tokenize("There are two doors, X and Y.")
#
# tagged = pos_tag(tokens)
# print(tagged)

from nltk import ne_chunk, pos_tag, word_tokenize,sent_tokenize
conditional_conjunctions = ['because', 'before', 'but', 'even if', 'if', 'if only', 'once', 'only if',
                            'on the condition that', 'provided', 'providing', 'since', 'therefore', 'unless',
                            'until', 'when','then']
example_sentence = "There are three sensors, X, Y and Z. Also there are three alarms, K, L and M . If Z or Y is giving a signal, then K is sounded. If Y or X is giving a signal, then L is sounded. If two or more sensors are giving a signal, then M is sounded."

tokn = [token for token in sent_tokenize(example_sentence)]
print(tokn)
focused = []
print(tokn.__len__())
for sent in tokn:
    lower_sent = sent.lower()
    print(sent)
    for word in conditional_conjunctions:
        if word in word_tokenize(lower_sent):
            focused.append(sent)
            break

print(list(set(tokn) - set(focused)))

#======================================
# token_sents = [pos_tag(word_tokenize(token)) for token in tokens ]
#
# nouns = []
# for word_token in token_sents:
#     nounList = []
#     for tag, pos in word_token:
#         if(pos == 'NNP' or pos == 'NNS') & (tag not in nounList):
#             nounList.append(tag)
#
#     nouns.append(nounList)
# print(nouns)
# reference_Dic ={}
# for nounList in nouns:
#     for noun in nounList:
#         pos = pos_tag(word_tokenize(noun))
#         if(pos[0][1]=="NNS"):
#             reference_Dic[pos[0][0]] = []
#             for word in nounList:
#                 if(word != pos[0][0]):
#                     reference_Dic[pos[0][0]].append(word)
#
# print(reference_Dic)
