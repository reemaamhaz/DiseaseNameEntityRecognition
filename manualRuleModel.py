import os
import sys
import nltk
import re

trainingFile = open("train.csv", 'r')
train = trainingFile.readlines()
trainingFile.close()

ncbi = open("/Users/reemaamhaz/Downloads/NCBI_corpus/NCBI_corpus_training.txt", 'r') 

devFile = open("dev.csv", 'r')
dev = devFile.readlines()
devFile.close()

# distant vision with NCBI
occurred = {}
pattern = r'<category="Modifier">(.*?)</category>'
disease = r'<category="SpecificDisease">(.*?)</category>'
disease_class = r'<category="DiseaseClass">(.*?)</category>'

for line in train:
    matches = re.findall(pattern, line, flags=re.DOTALL) + re.findall(disease, line, flags=re.DOTALL) +re.findall(disease_class, line, flags=re.DOTALL)
    for match in matches:
        list = match.split(" ")
        if list[0] not in occurred.keys():
            occurred[list[0]] = [list[0]]
        if len(list) > 1:
            for s in list[1:]:
                if s not in occurred[list[0]]:
                    occurred[list[0]].append(s)

#add all B, BI (as a phrase) to occurred
i=0
while i <len(train):
	train[i] = train[i].rstrip()
	entry = train[i].split(",")
	token = entry[3]
	BIO = entry[4]
	
	if BIO=="B-indications":
		temp = token
		j = i+1
		while j<len(train):
			tempAdd = train[j].rstrip().split(",")
			if tempAdd[4]=="I-indications":
				temp+= " "+tempAdd[3]
				j+=1
			else:
				break
		i = j
		if token in occurred:
			if temp not in occurred[token]:
				occurred[token].append(temp)
		else:
			occurred[token] = [temp]
	else:
		i+=1

i=0
while i<len(dev):
	dev[i] = dev[i].rstrip()
	entry = dev[i].split(",")
	token = entry[3]
	if token in occurred:
		#single word
		if token in occurred[token]:
			dev[i]+=",B-indications\n"
			i+=1
		#not single word, check up to bi-gram
		else:
			tempStr= token
			flag = False
			for j in range(i+1,i+3):
				if j>=len(dev):
					break
				dev[j] = dev[j].rstrip()
				tempEntry = dev[j].split(",")
				tempStr +=" "+tempEntry[3]
				if tempStr in occurred[token]:
					#mark i as B and i+1-j as I
					for k in range(i,j+1):
						if k==i:
							dev[k]+=",B-indications\n"
						else:
							dev[k]+=",I-indications\n"
					flag = True
					break
			if flag ==True:
				i = j+1
			else:
				dev[i]+=",O\n"
				i+=1
	else:
		dev[i] +=",O\n"
		i+=1

#write ans
ansFile = open("t.csv","w")
i=0
for i in range(len(dev)):
	ansFile.write(dev[i])
ansFile.close()









