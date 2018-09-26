#=================Text data aquisition process===============================
with open('data.txt', 'r') as myfile:
    example_sentence = myfile.read().replace('\n', '')

tt = example_sentence.split("Q.")
print(tt)
print(len(tt))

for i in tt:
    print(i)
    print("\n")
