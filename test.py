import sys, string

#open the results and the answer key for evaluation
data = open(sys.argv[1]).readlines()
answer_key = open(sys.argv[2]).readlines()

#create dictionaries of sentences and BIO tags
sent_id = 0
sentences = {}
bio_list = {}

#create empty lists for BIO tags and the words in each sentence
bio_tags = []
sentence = []
#for each word in list
for string in data:
    # split the data
    elements = string.split(",")
    # if the current sentence id = the previous sentence id it is the same sentence so append
    if (elements[2] == sent_id):
        bio_tags.append(elements[4][:-1])
        sentence.append(elements[3])
    #it's a new sentence so append to the dictionary and clear the lists
    else:
        sentences[sent_id] = sentence
        bio_list[sent_id] = bio_tags
        #set a new sentence id
        sent_id = elements[2]
        bio_tags = [elements[4][:-1]]
        sentence = [elements[3]]

# do the same for the answer key for comparison
#create dictionaries of sentences and BIO tags
ans_sent_id = 0
ans_sentences = {}
ans_bio_list = {}

#create empty lists for BIO tags and the words in each sentence
ans_bio_tags = []
ans_sentence = []
#for each word in list
for string in answer_key:
    # split the data
    ans_elements = string.split(",")
    # if the current sentence id = the previous sentence id it is the same sentence so append
    if (ans_elements[2] == ans_sent_id):
        ans_bio_tags.append(ans_elements[4][:-1])
        ans_sentence.append(ans_elements[3])
    #it's a new sentence so append to the dictionary and clear the lists
    else:
        ans_sentences[ans_sent_id] = ans_sentence
        ans_bio_list[ans_sent_id] = ans_bio_tags
        #set a new sentence id
        ans_sent_id = ans_elements[2]
        ans_bio_tags = [ans_elements[4][:-1]]
        ans_sentence = [ans_elements[3]]

exact = 0
fn = 0
fp = 0
of = 0
# loop through the BIO tag lists for each sentence and compare to the answer key
for key in bio_list:
    for i in range(len(bio_list[key])):
        if (bio_list[key][i] == ans_bio_list[key][i]):
            exact += 1
        elif (bio_list[key][i] == "O"):
            fn += 1
            print(sentences[key][i])
        elif (bio_list[key][i] == "B-indications" or bio_list[key][i] == "I-indications"):
            fp += 1
print(float(fn))
print(fp)
precision = 0
recall = 0
f1 = 0

precision = float(exact)/float(exact + fp)
recall = float(exact)/float(exact + fn)
f1 = (2 * precision * recall)/(precision + recall)

print("Precision: ")
print(precision)
print("Recall: ")
print(recall)
print("F1: ")
print(f1)