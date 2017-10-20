from Ngram import V_size,Read_test_Data, Vocabulary,Trigram_Counter, Bigram_Counter, Unigram_Counter
#from Ngram import Read_test_Data
from nltk.util import ngrams
import math
import random

"""
Randome pick an item according to it's probability
Input: some_list: list, with all the items
       probabilities: list, with the corresponded prob
output: an item
"""
def random_pick(some_list, probabilities):
    x = random.uniform(0,1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:break
    return item



print "------------------Generate Sentence-------------------------"


Trigram_Keys = Trigram_Counter.keys()
Bigram_Keys = Bigram_Counter.keys()
Unigram_Keys = Unigram_Counter.keys()
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

'''Compute the Tri_prob for generate sentence'''
Tri_prob = []
for key in Trigram_Keys:
    prob = (Trigram_Counter[key] + 1.0) / (Bigram_Counter[(key[0], key[1])] + V_size)
    Tri_prob.append(prob)

Total = 0
for i in Tri_prob:
    Total += i
Tri_prob_1 = [i*1.0 / Total for i in Tri_prob]


print "===============add1 Generate sentence============="
'''
Generate sentence from LM
Input: Trigram_Keys: list, all trigram tokens
       Tri_prob: list, corresponed weights
'''

'''
Compute the probability of a token elem = (w1,w2,w3)
'''
def get_prob(elem):
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
    return temp

def Generate_S():
    sentence = ''
    start_Keys = []  # All the trigram tokens start with '<s>', eg: ('<s>','I','know')
    start_prob = []  # corresponded probability
    for i in range(0,len(Trigram_Keys)):
        if Trigram_Keys[i][0] == '<s>' and Trigram_Keys[i][1] == '<s>':
            start_Keys.append(Trigram_Keys[i])
            start_prob.append(Tri_prob[i])
    '''Normalization'''
    Total = 0
    for i in start_prob:
        Total += i
    start_prob_1 = [i*1.0 / Total for i in start_prob]
    Symbol = (1, 2)
    for i in range(0, 100000000):
        if i == 0:
            str = random_pick(start_Keys, start_prob_1)
            if str[2] != '</s>':
                sentence += ' ' + str[0] + ' ' + str[1] + ' ' + str[2]
                Symbol = (str[1], str[2])
            else:
                sentence += ' ' + str[0] + ' ' + str[1] + ' ' + str[2]
                break

        if Symbol == (1, 2):
            str = random_pick(Trigram_Keys, Tri_prob)
            if str[2] != '</s>':
                sentence += ' ' + str[0] + ' ' + str[1] + ' ' + str[2]
                Symbol = (str[1], str[2])
            else:
                sentence += ' ' + str[0] + ' ' + str[1] + ' ' + str[2]
                break
        else:
            new_Tigram = []
            new_prob = []
            for uni_token in Unigram_Keys:
                elem = (Symbol[0],Symbol[1],uni_token[0])
                new_Tigram.append(elem)
                new_prob.append(get_prob(elem))
            str = random_pick(new_Tigram,new_prob)
            if str[2] != '</s>':
                sentence += ' ' + str[2]
                Symbol = (str[1], str[2])
            else:
                sentence += ' ' + str[2]
                break

    print sentence


for i in range(0,20):
    print "Generating the ",i," sentence"
    Generate_S()

print "===============/Generate sentence============="
