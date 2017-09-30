import csv
import pandas as pd



DIR = ''
fname = 'train.counts'
fpath = DIR+fname
#read file
rows = []
f=open(fpath, 'rb')
lines = f.readlines()
f.close()
#remove '\n'
for line in lines:
    line = line.rstrip('\n')
    rows.append([line])

Emission_count = [row[0].split() for row in rows[:22189]] # Read the text and remove all the unnecessary symbols
Bigram_count = [row[0].split() for row in rows if row[0].strip().split()[1] == "2-GRAM"]

print Emission_count[:3]
print Bigram_count[:3]

#coumpute the tags and theri counts, eg:[['ADV', 10551], ['NOUN', 35315], ['ADP', 17640]]
tag = []    #all the appeared tags
for w in Emission_count:
    tag.append(w[2])
tag_no_rep = list(set(tag)) #remove the reprtition
tag_count = [[i,0] for i in tag_no_rep]
for element in Emission_count:
    tag_count[tag_no_rep.index(element[2])][1] += eval(element[0])
#print tag_count
#tag_count is: [['ADV', 10551], ['NOUN', 35315], ['ADP', 17640], ['PRON', 17183], ['SCONJ', 3842], ['PROPN', 12945], ['DET', 17148], ['SYM', 598], ['INTJ', 688], ['PART', 5564], ['PUNCT', 23680], ['NUM', 3999], ['AUX', 7895], ['X', 848], ['CONJ', 6707], ['ADJ', 12475], ['VERB', 27508]]
#tag_no_rep is: ['ADV', 'NOUN', 'ADP', 'PRON', 'SCONJ', 'PROPN', 'DET', 'SYM', 'INTJ', 'PART', 'PUNCT', 'NUM', 'AUX', 'X', 'CONJ', 'ADJ', 'VERB']


####################################################################
###Question 4, part 1
###Emission_Prob function: Compute emission probabilities
###input: dataset of a list, with the form of [['<count>', 'WORDTAG', '<tag>', '<word>'],...]
###output: emission prob result, list with the form of [['<word>', '<tag>', prob value],...]
###################################################################
def Emission_Prob(Emission_count):
    word = []   #all the appeared words
    tag = []    #all the appeared tags
    word_count = []     #word_count list

    for w in Emission_count:
        word.append(w[3])
        tag.append(w[2])
        word_count.append([w[3],w[2],eval(w[0])])

    word_no_rep = list(set(word)) #remove the repetition
    tag_no_rep = list(set(tag)) #remove the reprtition
    tag_sum = [[i,0] for i in tag_no_rep]

    for element in Emission_count:
        tag_sum[tag_no_rep.index(element[2])][1] += eval(element[0])

    #compute the emission prob

    for element in word_count:
        j = tag_no_rep.index(element[1])
        #print "j: ",j
        temp = element[2]*1.0
        #print temp,tag_sum[j][1]
        element[2] = temp/(tag_sum[j][1])

    return word_count
"""
emission_prob = Emission_Prob(Emission_count)
print emission_prob[:10]

"""
####################################################################
###Question 4, part2
###Transition_Prob function: Compute transition probabilities
###input: a list of 2-gram counts, with the form of [['433', '2-GRAM', 'PART', 'NOUN'], ['625', '2-GRAM', 'PUNCT', 'ADP'], ['445', '2-GRAM', 'VERB', 'VERB']]
###output: transition prob result, list with the form of [[prob(tag1,tag2), '<tag1>', '<tag2>'],...]
###################################################################
def Transition_Prob(Bigram_count):
    Bigram_tag = [[t[0],t[2],t[3]] for t in Bigram_count] #eg: [['433', 'PART', 'NOUN'], ['625', 'PUNCT', 'ADP'], ['445', 'VERB', 'VERB'],...]
    tran_prob = []
    for elem in Bigram_tag:
        if elem[1]!='*':
            prob = (eval(elem[0]) * 1.0) / tag_count[tag_no_rep.index(elem[1])][1]
            tran_prob.append([prob,elem[1],elem[2]])
    return tran_prob

tran_prob = Transition_Prob(Bigram_count)
#print tran_prob