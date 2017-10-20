import csv
import collections
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import re
import string


"""
traintext = ["hi ya. see you tomorrow. it's fine, thank you. my name is blah blah blah. attention to the words...","What kind of experience [ do you, + do you ] have, then with child care? "]
testtext = "This is fine, thank you"

token_train = [word_tokenize(i) for i in traintext]
token_test = word_tokenize(testtext)
model = ngrams(token_train, 3)

print token_train
print list(model)
"""


#------------------------------------------------
#Read data from csv file
#Remove unnecessary symbols
#Lower the words
#-------------------------------------------------
DIR = 'q3_lm/'
fname = 'train_set.csv'
fpath = DIR+fname


def toLowerCase(s):
    #Convert a sting to lowercase. E.g., 'BaNaNa' becomes 'banana'

    return s.lower()


def stripNonAlpha(s):
    # Remove non alphabetic characters. E.g. 'B:a,n+a1n$a' becomes 'Banana'
    return ''.join([c for c in s if (c.isalpha() or c == "'") ] )


####################################################################
###Read_train_Data function: Read text data from csv file and return a list with tokenized words
###input: csv file path
###output: list  eg:['UNK','okay'], ['so'], ['guess'],...], and vocabulary size
###################################################################
def Read_train_Data(fpath):

    with open(fpath, 'rb') as csvfile:
        mreader = csv.reader(csvfile)
        rows = [row for row in mreader]
        # column = [row[0] for row in mreader]

    RE_1 = re.compile("<(.*)>")
    RE_2 = re.compile("<<(.*)>>")
    RE_3 = re.compile("{[A-Z]")
    #RE_3 = re.compile("{(.*)}")
    column = []
    for row in rows[1:]:
        text1 = RE_1.sub('',row[8])
        text2 = RE_2.sub('',text1)
        text3 = RE_3.sub('',text2).strip()
        column.append([text3])
    #column = [[row[8]o.strip()] for row in rows] # Read the text and remove all the unnecessary symbols.[['text'], ['<laughter> {C or } the phone rang [ or, + ]'], ['<Laughter>.'], ['{D you know, } at the wrong time <laughter>. /'], ['Yeah. /']]
    column_token = [ele[0].split() for ele in column]
    #column_split = [word_tokenize(ele[0]) for ele in column_addToken]

    #remove the background, like '<laugh>',and some single word in {}
    print "tokenize"
    column_token_process = []
    for element in column_token:
        temp = []
        """
        for i in element:
            if re.findall("(.*){(.*)",i):
            #if re.findall("<(.*)>",i) or re.findall("(.*){(.*)",i):
                continue
            else:
                temp += word_tokenize(i)
        """
        for i in element:
            if (len(i) ==1 and i not in string.punctuation) or len(i)>1: # condition1: i is single word, like 'I', 'a'; condition 2: i is a word, eg:'apple', 'apple.'
                if i[-1] in string.punctuation:
                    temp += [i[0:-1]]
                    temp += [i[-1]]
                else:
                    temp += [i]
            #temp += word_tokenize(i)
        column_token_process.append(temp)

    print "add start and end tags"
    processed_data = []
    for elem in column_token_process:
        temp = ['<s>', '<s>']
        for i in elem:
            if len(i) > 1:
                j = stripNonAlpha(i)
                if j != '':
                    if len(j) != 1:
                        temp.append(toLowerCase(j))
                    else:
                        temp.append(j)
            else:
                temp.append(i)
        temp.append('</s>')
        processed_data.append(temp)

    #data_count: remove the inner list of processed_data, eg:['a','a','b','f'...]
    data_count = []
    for data_tempi in processed_data:
        for data_tempj in data_tempi:
            data_count.append(data_tempj)


    Vocabulary = [] #Create the vocabulary of train data
    d = collections.Counter(data_count)#d is a dict: ({'a': 2, 'b': 2, 'c': 1})
    print "the length of V before UNK: ",len(d)
    UNK_word = []
    for k in d:
        if d[k] < 5:
            UNK_word.append(k)
        else:
            Vocabulary.append(k)

    UNK_word = set(UNK_word)
    print "UNK process"
    #final_data is the processed_data with UNK
    final_data = []
    for temp_1 in processed_data:
        temp = []
        for temp_2 in temp_1:
            if temp_2 in UNK_word:
                temp_2 = 'UNK'
            temp.append(temp_2)
        final_data.append(temp)

    V_size = len(d) - len(UNK_word) + 1
    print "The path of the file is :",fpath
    return final_data, V_size, Vocabulary

#train_set = Read_Data(fpath)
#print "Read_data: ",train_set[:10]



####################################################################
###Read_test_Data function: Read text data from csv file and return a list without tokenized words
###input: csv file path
###output: list  eg:['I','okay'], ['so'], ['guess'],...], and vocabulary size
###################################################################
def Read_test_Data(fpath):

    with open(fpath, 'rb') as csvfile:
        mreader = csv.reader(csvfile)
        rows = [row for row in mreader]
        # column = [row[0] for row in mreader]

    RE_1 = re.compile("<(.*)>")
    RE_2 = re.compile("<<(.*)>>")
    RE_3 = re.compile("{[A-Z]")
    #RE_3 = re.compile("{(.*)}")
    column = []
    for row in rows[1:]:
        text1 = RE_1.sub('',row[8])
        text2 = RE_2.sub('',text1)
        text3 = RE_3.sub('',text2).strip()
        column.append([text3])
    #column = [[row[8]o.strip()] for row in rows] # Read the text and remove all the unnecessary symbols.[['text'], ['<laughter> {C or } the phone rang [ or, + ]'], ['<Laughter>.'], ['{D you know, } at the wrong time <laughter>. /'], ['Yeah. /']]
    column_token = [ele[0].split() for ele in column]
    #column_split = [word_tokenize(ele[0]) for ele in column_addToken]

    #remove the background, like '<laugh>',and some single word in {}
    print "tokenize"
    column_token_process = []
    for element in column_token:
        temp = []
        """
        for i in element:
            if re.findall("(.*){(.*)",i):
            #if re.findall("<(.*)>",i) or re.findall("(.*){(.*)",i):
                continue
            else:
                temp += word_tokenize(i)
        """
        for i in element:
            if (len(i) ==1 and i not in string.punctuation) or len(i)>1:
                if i[-1] in string.punctuation:
                    temp += [i[0:-1]]
                    temp += [i[-1]]
                else:
                    temp += [i]
            #temp += word_tokenize(i)
        column_token_process.append(temp)

    print "add start and end tags"
    processed_data = []
    for elem in column_token_process:
        temp = ['<s>','<s>']
        for i in elem:
            if len(i) > 1:
                j = stripNonAlpha(i)
                if j != '':
                    if len(j)!=1 :
                        temp.append(toLowerCase(j))
                    else:
                        temp.append(j)
            else:
                temp.append(i)
        temp.append('</s>')
        processed_data.append(temp)

    print "The path of the file is :",fpath
    return processed_data

####################################################################
###Ngram function: Ngram language model implementation
###input: dataset: list eg:[['UNK'], ['okay'], ['so'], ['guess','what','UNK']]
###output:  Counter, which is like a dictionary. With the keys to be N-gram tokens, value to be the number of each token.
###################################################################
def Ngram(dataset,N):
    Ngram_result = []
    for data in dataset:
        n_gram = list(ngrams(data,N))
        if n_gram!=[]:
            for result in n_gram:
                Ngram_result.append(result)
    size = len(list(set(Ngram_result)))
    if N == 1:
        print "Unigram: ",len(Ngram_result)
    return collections.Counter(Ngram_result)



print "--------------Ngram Read Data---------------------"
train_set,V_size,Vocabulary = Read_train_Data(fpath)
print "length of train_set: ",len(train_set),train_set[:10]
print "V size: ",V_size
print "The first 5 elements in train set: ",train_set[:5]

print "-------------Trigram Process-------------------------"
Trigram_Counter = Ngram(train_set,3)
print "Trigram: ",Trigram_Counter.keys()[:10]
print "|Trigram_size|: ", len(Trigram_Counter)


print "-------------Bigram Process-------------------------"
Bigram_Counter = Ngram(train_set,2)
print "Bigram: ",Bigram_Counter.keys()[:10]
print "|Bigram_size|: ", len(Bigram_Counter)

print "-------------Unigram Process-------------------------"
Unigram_Counter = Ngram(train_set,1)
print "Unigram: ",Unigram_Counter.keys()[:10]
print "|Unigram_size|: ", len(Unigram_Counter)






