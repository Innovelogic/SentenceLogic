import re
sentence = "I love downloading iPhone games from my mac."
query = r'((iphone|games|mac)\s*)+'
regex = re.compile(query, re.I)
sentence = regex.sub(r'<em>\1</em> ', sentence)
print(sentence)