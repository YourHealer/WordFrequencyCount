from nltk.stem import WordNetLemmatizer
from zhon.hanzi import punctuation
from collections import Counter
from nltk.book import *
import string
import nltk
import csv
import re

# 按照词频排序
def sort_by_wordFrequency(d):
    '''
    d.items() 返回元素为 (key, value) 的可迭代类型（Iterable），
    key 函数的参数 k 便是元素 (key, value)，所以 k[0] 取到字典的键。
    '''
    # lambda表达式多字段排序
    return sorted(d.items(), key=lambda k: (k[1][0], k[0]), reverse=True)

# 加载语料库
nltk.download('wordnet')
wnl = WordNetLemmatizer()

# 打开文件
f = open('docu.txt', encoding='utf-8')

# 建立词语-词频 词语-题号 两个字典
counter_num = {}
counter_pos = {}

# 将每句话视作列表res的元素，每个元素又包括题号和原句两部分
res = []
for line in f:
    dic = [0, 0]
    dic[0] = line.strip()[1:8]
    dic[1] = line.strip()[9:].lower()
    res.append(dic)

# 对每个句子进行分析，先去除标点符号
for ele in res:
    # mylist = ['.', '“', '”', ':', '(', ')', '"', '\"', '>', '，', ',', '...','%',';',]
    # for i in mylist:
    #     ele[1] = ele[1].strip(i)
    punctuation_string = string.punctuation
    ele[1] = re.sub('[{}]'.format(punctuation_string), " ", ele[1])

    ele[1] = re.sub('[{}]'.format(punctuation), " ", ele[1])

    ele[1] = re.sub('[\d]', ' ', ele[1])

    ele[1] = re.sub('[\u4e00-\u9fa5]', ' ', ele[1])
    # 将得到的去除标点符号的句子进行切分
    words = ele[1].split()

    # 得到切分后的列表中各词语的词性
    pos_tags = nltk.pos_tag(words)

    # 为每个句子建立记录词频和位置的字典
    num = {}
    pos = set()

    # 对每个单词进行分析，还原其原形（形容词、副词还原至原形，动词去除时态，名词变为单数等）
    for i in range(len(words)):
        if pos_tags[i][1].startswith('J'):  # 形容词
            origin = wnl.lemmatize(words[i], wordnet.ADJ)
        elif pos_tags[i][1].startswith('V'):  # 动词
            origin = wnl.lemmatize(words[i], wordnet.VERB)
        elif pos_tags[i][1].startswith('N'):  # 名词
            origin = wnl.lemmatize(words[i], wordnet.NOUN)
        elif pos_tags[i][1].startswith('R'):  # 副词
            origin = wnl.lemmatize(words[i], wordnet.ADV)
        else:  # 其他词
            origin = words[i]

        num[origin] = 1
        # 记录该句中所有出现的词语
        pos.add(origin)

    # 字典值加和，记录单词的总出现次数
    X, Y = Counter(counter_num), Counter(num)
    counter_num = dict(X + Y)

    # 若没有建立字典，若有则补充
    for index in pos:
        if index not in counter_pos.keys():
            counter_pos[index] = [ele[0]]
        else:
            counter_pos[index].append(ele[0])

final = {}
for i in counter_num.keys():
    final[i] = [counter_num[i], counter_pos[i]]

# 输出
final = dict(sort_by_wordFrequency(final))
print(final)

# 写入csv文件
file = open('wordFrequency.csv', 'w', encoding='utf-8', newline='' "")
csv_writer = csv.writer(file)
csv_writer.writerow(["单词", "词频", "年份"])
for ke in final.keys():
    csv_writer.writerow([ke, final[ke][0], final[ke][1]])

file.close()
