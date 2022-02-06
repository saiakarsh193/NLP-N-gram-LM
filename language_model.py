import sys
import random
import math
import os
from tokenizer import tokenize

class LanguageModel():
    def __init__(self, ngram, smooth, path):
        self.ngram = ngram
        self.smooth = self.checkSmoothType(smooth)
        self.rawdata = self.readFile(path)
        self.train_data, self.raw_train_data, self.raw_test_data = self.splitTrainTestandTokenize(1000, -1)
        self.vocab, self.vocab_length, self.vocab_length_total = self.makeVocabulary()
        self.train()

    def checkSmoothType(self, smooth):
        smooth = smooth.lower()
        if(smooth == 'k' or smooth == 'kneser' or smooth == 'ney' or smooth == 'kneser ney' or smooth == 'kneser-ney'): # Kneser-Ney Smoothing
            return 'k'
        elif(smooth == 'w' or smooth == 'witten' or smooth == 'bell' or smooth == 'witten bell' or smooth == 'witten-bell'): # Witten-Bell Smoothing
            return 'w'
        else: # Laplace Smoothing
            return 'l'

    def readFile(self, path):
        with open(path, 'r') as f:
            lne = f.readlines()
        return lne

    def tokenizeDataset(self, dataset):
        tokenlist = []
        for sentence in dataset:
            tokenlist.append(tokenize(sentence.strip()))
        return tokenlist

    def splitTrainTestandTokenize(self, test_count, random_seed):
        if(random_seed >= 0):
            random.seed(random_seed)
        random.shuffle(self.rawdata)
        return self.tokenizeDataset(self.rawdata[test_count:]), self.rawdata[test_count:], self.rawdata[0:test_count]

    def makeVocabulary(self):
        vocab = {}
        t_cnt = 0
        for tokens in self.train_data:
            for token in tokens:
                t_cnt += 1
                if token in vocab:
                    vocab[token] += 1
                else:
                    vocab[token] = 1
        uk_cnt = 0
        for key, val in list(vocab.items()):
            if(val == 1):
                del vocab[key]
                uk_cnt += 1
        vocab['<UNKNOWN>'] = uk_cnt
        return vocab, len(vocab.keys()), t_cnt

    def updateUnkSentence(self, tokens):
        return [(token if token in self.vocab else '<UNKNOWN>') for token in tokens]

    def train(self):
        tmodel = {}
        for tokens in self.train_data:
            tokens = self.updateUnkSentence(tokens)
            temp = (['<START>'] * (self.ngram - 1)) + tokens
            for n in range(1, self.ngram):
                for i in range(self.ngram - 1, len(temp)):
                    base = ' '.join(temp[i - n: i])
                    word = temp[i]
                    if(base not in tmodel):
                        tmodel[base] = {"<TOTAL_COUNT>": 0}
                    if(word != "<TOTAL_COUNT>"):
                        if(word not in tmodel[base]):
                            tmodel[base][word] = 0
                        tmodel[base][word] += 1
                        tmodel[base]["<TOTAL_COUNT>"] += 1
        for key in tmodel.keys():
            tmodel[key]["<UNIQUE_COUNT>"] = len(tmodel[key].keys()) - 1
        self.tmodel = tmodel

    def lapProbFunc(self, word, base):
        if(base in self.tmodel):
            cbase = self.tmodel[base]["<TOTAL_COUNT>"]
        else:
            cbase = 0
        if(word != "<TOTAL_COUNT>" and word != "<UNIQUE_COUNT>" and cbase > 0 and word in self.tmodel[base]):
            ctotal = self.tmodel[base][word]
        else:
            ctotal = 0
        pw = (1 + ctotal) / (self.vocab_length + cbase)
        return pw

    def witProbFunc(self, word, base):
        if(len(base) == 0):
            return self.vocab[word] / self.vocab_length_total
        jbase = ' '.join(base)
        if(jbase in self.tmodel and word in self.tmodel[jbase]):
            blamb = self.tmodel[jbase]["<UNIQUE_COUNT>"] / (self.tmodel[jbase]["<UNIQUE_COUNT>"] + self.tmodel[jbase]["<TOTAL_COUNT>"])
            alamb = 1 - blamb
            return alamb * (self.tmodel[jbase][word] / self.tmodel[jbase]["<TOTAL_COUNT>"]) + blamb * self.witProbFunc(word, base[1:])
        else:
            return self.witProbFunc(word, base[1:])

    def getProb(self, word, base):
        if(self.smooth == 'l'):
            return self.lapProbFunc(word, ' '.join(base))
        if(self.smooth == 'w'):
            return self.witProbFunc(word, base)

    def getPerplexity(self, sentence, prob=False):
        temp = self.updateUnkSentence(tokenize(sentence.strip()))
        n = len(temp)
        temp = (['<START>'] * (self.ngram - 1)) + temp
        ppw = 1
        for i in range(self.ngram - 1, len(temp)):
            base = temp[i - (self.ngram - 1): i]
            word = temp[i]
            ppw *= self.getProb(word, base)
        if(not prob):
            try:
                ppw = math.pow(ppw, -1/n)
            except Exception as exception:
                ppw = 1
        return ppw

    def log(self, value = ''):
        roll = '2019111017'
        if(not os.path.isdir('./logs')):
            os.mkdir('./logs')
        tsum = 0
        tstr = ""
        for sentence in self.raw_train_data:
            ppw = self.getPerplexity(sentence)
            tsum += ppw
            tstr += sentence[:-1] + "\t" + str(ppw) + "\n"
        tsum = tsum / len(self.raw_train_data)
        with open('logs/' + roll + '_LM' + value + '_train-perplexity.txt', 'w') as f:
            f.write(str(tsum) + "\n" + tstr)
        tsum = 0
        tstr = ""
        for sentence in self.raw_test_data:
            ppw = self.getPerplexity(sentence)
            tsum += ppw
            tstr += sentence[:-1] + "\t" + str(ppw) + "\n"
        tsum = tsum / len(self.raw_test_data)
        with open('./logs/' + roll + '_LM' + value + '_test-perplexity.txt', 'w') as f:
            f.write(str(tsum) + "\n" + tstr)

if(len(sys.argv) == 4):
    lm = LanguageModel(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    # uncomment this line to log the perplexity values for train and test set
    # lm.log("") # the parameter is LM id value for naming the file
    while True:
        tstr = input("input sentence: ")
        print(lm.getPerplexity(tstr, prob=True))
else:
    print("Invalid number of parameters")