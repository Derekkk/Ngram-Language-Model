from Ngram import V_size,Read_test_Data, Vocabulary,Trigram_Counter,Bigram_Counter,Unigram_Counter
#from Ngram import Read_test_Data
from nltk.util import ngrams
import math


print "------------------add1 perplexity-------------------------"


Trigram_Keys = Trigram_Counter.keys()
Bigram_Keys = Bigram_Counter.keys()
Unigram_Keys = Unigram_Counter.keys()
#print Trigram_Keys
#print Bigram_Keys
#print Unigram_Keys

Uni_count = 0
for key in Unigram_Keys:
    Uni_count += Unigram_Counter[key]
print "Uni_count: ",Uni_count
#test_data = ['<s>','the','phone','rang','or','.','</s>']
#test_data = [('<s>','the','phone'),('the','phone','rang'),('phone','rang','or'),('rang','or','.'),('or','.','</s>')]


def test_Prob(test_data,lam1,lam2,lam3):
    prob = 1
    for elem in test_data:
        if Trigram_Counter.has_key(elem):
            prob_tri = Trigram_Counter[elem]*1.0 / Bigram_Counter[(elem[0],elem[1])]
        else:
            prob_tri = 0
        if Bigram_Counter.has_key((elem[1],elem[2])):
            prob_bi = Bigram_Counter[(elem[1],elem[2])]*1.0 / Unigram_Counter[(elem[1],)]
        else:
            prob_bi = 0
        prob_uni = Unigram_Counter[(elem[2],)]*1.0 / Uni_count
        '''
        print "tri:", prob_tri
        print "bi:", prob_bi
        print "uni:", prob_uni
        '''
        temp = lam3*prob_uni + lam2*prob_bi + lam1*prob_tri
        #print temp
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
    Trigram_test.append(list(ngrams(i,3)))

print "test_trigram: ",Trigram_test[:10]


print "---------------------Perplexity----------------------------"
Prob = 0
Counter = 0

for testdata in Trigram_test:
    Prob += test_Prob(testdata, 0.3, 0.4, 0.3)
    Counter += 1
print Prob / len(Trigram_test)
print Prob / Counter
"""
print test_Prob(Trigram_test[0],0.2,0.2,0.4)
"""
