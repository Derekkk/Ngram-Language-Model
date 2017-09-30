import csv
import collections
import nltk
from nltk import word_tokenize
from nltk.util import ngrams


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
    return ''.join([c for c in s if c.isalpha()])

####################################################################
###Read_Data function: Read text data from csv file and return a list with tokenized words
###input: csv file path
###output: list  eg:['UNK','okay'], ['so'], ['guess'],...]
###################################################################
def Read_Data(fpath):

    with open(fpath, 'rb') as csvfile:
        mreader = csv.reader(csvfile)
        rows = [row for row in mreader]
        # column = [row[0] for row in mreader]

    column = [[row[8]] for row in rows] # Read the text and remove all the unnecessary symbols
    column_split = [c[0].split() for c in column] #split the sentence

    #processed data, without UNK, eg:[['a','b'],['a'],['f']...]
    processed_data = []

    for data in column_split:
        temp = []
        for i in data:
            i = toLowerCase(i)
            i = stripNonAlpha(i)
            if len(i)>1:
                temp.append(i)
        processed_data.append(temp)

    #data_count: remove the inner list of processed_data, eg:['a','a','b','f'...]
    data_count = []
    for data_tempi in processed_data:
        for data_tempj in data_tempi:
            data_count.append(data_tempj)

    d = collections.Counter(data_count)
    UNK_word = []
    for k in d:
        if d[k] < 5:
            UNK_word.append(k)

    #final_data is the processed_data with UNK
    final_data = []
    for temp_1 in processed_data:
        temp = []
        for temp_2 in temp_1:
            if temp_2 in UNK_word:
                temp_2 = 'UNK'
            temp.append(temp_2)
        final_data.append(temp)

    print "The path of the file is :",fpath
    return final_data


####################################################################
###Trigram function: trigram language model implementation with NLTK
###input: dataset: list eg:[['UNK'], ['okay'], ['so'], ['guess','what','UNK']]
###output: list(Trigram),n(vocabulary size)   eg:[('what', 'kind', 'of'), ('kind', 'of', 'experience'), ('of', 'experience', 'do')]
###################################################################
def Trigram(dataset):
    Trigram_result = []
    for data in dataset:
        tri_gram = list(ngrams(data,3))
        if tri_gram!=[]:
            for result in tri_gram:
                Trigram_result.append(result)
    n = len(list(set(Trigram_result)))
    return Trigram_result,n

train_set = Read_Data(fpath)
print len(train_set)
print train_set[:5]

Trigram_Model, V = Trigram(train_set)
print "Trigram: ",len(Trigram_Model),Trigram_Model[0:5]
print "|V|: ", V

