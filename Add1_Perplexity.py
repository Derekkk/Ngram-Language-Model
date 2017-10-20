from Ngram import V_size,Read_test_Data, Vocabulary,Trigram_Counter
#from Ngram import Read_test_Data
from nltk.util import ngrams
import math


print "------------------add1 perplexity-------------------------"


Trigram_Keys = Trigram_Counter.keys()
#Bigram_Keys = Bigram_Counter.keys()
#nigram_Keys = Unigram_Counter.keys()
#print Trigram_Keys
#print Bigram_Keys
#print Unigram_Keys

'''Compute the C(c1,c2)'''
Bigram_Counter = {}
for key in Trigram_Keys:
    if Bigram_Counter.has_key((key[0],key[1])):
        Bigram_Counter[(key[0],key[1])] += Trigram_Counter[key]
    else:
        Bigram_Counter[(key[0], key[1])] = Trigram_Counter[key]


#test_data = ['<s>','the','phone','rang','or','.','</s>']
#test_data = [('<s>','the','phone'),('the','phone','rang'),('phone','rang','or'),('rang','or','.'),('or','.','</s>')]

def test_Prob(test_data):
    prob = 1
    for elem in test_data:
        temp = 0
        if Trigram_Counter.has_key(elem):
            #print "Trigram_Counter.has_key(elem)",elem
            temp = (Trigram_Counter[elem]+1.0) / (Bigram_Counter[(elem[0],elem[1])]+V_size)
        else:
            if Bigram_Counter.has_key((elem[0],elem[1])):
                #print "Bigram_Counter.has_key((elem[0],elem[1]))",elem,Bigram_Counter[(elem[0],elem[1])]
                temp = (0 + 1.0) / (Bigram_Counter[(elem[0],elem[1])]+V_size)
            else:
                temp = (0 + 1.0) / (0 + V_size)

        #print temp, elem
        prob = prob * temp
    N = len(test_data)
    #print N, prob
    return math.pow(prob,-1.0/N)


print "--------------Read test Data---------------------"
DIR = 'q3_lm/'
fname = 'test_set.csv'

test_set= Read_test_Data(DIR +fname)
print "length of test_set: ",len(test_set)

print "The first 5 elements in test set: ",test_set[:5]
print "-------------test data Process-------------------------"
vocabulary = set(Vocabulary)
print Vocabulary[:10]
test_set_UNK = []
for elem in test_set:
    temp = []
    for word in elem:
        if word not in vocabulary:
            word = 'UNK'
            temp.append(word)
        else:
            temp.append(word)
    test_set_UNK.append(temp)
print "The first 5 elements in test set after UNK: ",test_set_UNK[:5]
Trigram_test = []
for i in test_set_UNK:
    if len(i) >3 :
        Trigram_test.append(list(ngrams(i,3)))

print "test_trigram: ",Trigram_test[:10]


print "---------------------Perplexity----------------------------"
Prob = 0
Counter = 0
position = 0

for testdata in Trigram_test:
    Prob += test_Prob(testdata)
    Counter += 1
    position += 1
print Prob / len(Trigram_test)
print Prob / Counter


#print test_Prob(Trigram_test[4217])

