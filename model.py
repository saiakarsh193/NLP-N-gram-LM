from tokenizer import tokenize
import math

lm_dict = {}

def addToDict(tokens):
    global lm_dict
    n = 4
    for i in range(len(tokens)):
        for j in range(n):
            if(i + j + 1 <= len(tokens)):
                tmp = " ".join(tokens[i: i + j + 1])
                if(tmp in lm_dict):
                    lm_dict[tmp] += 1
                else:
                    lm_dict[tmp] = 1

def tokenize_file(path, count = -1):
    with open(path, 'r') as f:
        lne = f.readline()
        while(lne != "" and count != 0):
            addToDict(tokenize(lne.strip()))
            lne = f.readline()
            count -= 1

def validPer(text):
    global lm_dict
    n = 4
    tk = tokenize(text)
    per = 1
    for ind, word in enumerate(tk):
        if(ind - n + 1 < 0):
            bs = tk[:ind]
        else:
            bs = tk[ind - n + 1:ind]
        bs = ' '.join(bs)
        if(bs != ""):
            tot = bs + ' ' + word
            if(bs in lm_dict and tot in lm_dict):
                per *= 1 / (lm_dict[tot] / lm_dict[bs])
    return math.pow(per, 1 / len(tk))

tokenize_file('corpus/general-tweets.txt')
# tokenize_file('corpus/medical-corpus.txt')
# tokenize_file('temp.txt')

# print(len(lm_dict.keys()))
# for ind, (key, value) in enumerate(sorted(lm_dict.items(), key=lambda item: item[1], reverse=True)):
#     if(ind < 40):
#         print(key, ' :: ', value)

print(validPer("The patient is sick!"))
print(validPer("#GokulGiri is awesome!!!"))