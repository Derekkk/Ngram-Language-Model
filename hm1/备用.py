#读文件部分
"""

with open(fpath, 'rb') as csvfile:

    mreader = csv.reader(csvfile)

    rows = [row for row in mreader]
    #column = [row[0] for row in mreader]

column = [[row[8]] for row in rows]

column_split = [c[0].split() for c in column]

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

print "processed_data: ",len(processed_data),processed_data[:10]

#data_count: remove the inner list of processed_data, eg:['a','a','b','f'...]
data_count = []
for data_tempi in processed_data:
    for data_tempj in data_tempi:
        data_count.append(data_tempj)

d = collections.Counter(data_count)
print "d: ",len(d)
print d['range']
UNK_word = []
for k in d:
    if d[k] < 5:
        UNK_word.append(k)
print len(UNK_word)
print UNK_word[:20]

final_data = []
for temp_1 in processed_data:
    temp = []
    for temp_2 in temp_1:
        if temp_2 in UNK_word:
            temp_2 = 'UNK'
        temp.append(temp_2)
    final_data.append(temp)

print "final_data: ",len(final_data),final_data[:10]
"""