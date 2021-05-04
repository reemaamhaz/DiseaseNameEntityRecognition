import sys, string
import re

train= open("/Users/reemaamhaz/Downloads/NCBI_corpus/NCBI_corpus_training.txt", 'r') 

# distant vision with data
occurred = {}
pattern = r'Andromeda'
gen = r'galaxy'

for line in train:
    matches = re.findall(pattern, line, flags=re.DOTALL) + re.findall(gen, line, flags=re.DOTALL)
    for match in matches:
        if list[0] not in occurred.keys():
            occurred[list[0]] = [list[0]]
            occurred[list[0]].append("")
        if len(list) > 1:
            for s in list[1:]:
                if s not in occurred[list[0]]:
                    occurred[list[0]].append(s.lower())
print(occurred)