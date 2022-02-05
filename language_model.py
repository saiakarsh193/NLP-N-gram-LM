import sys
import random
from tokenizer import tokenize

class LanguageModel():
    def __init__(self, ngram, smooth, path):
        self.ngram = ngram
        self.smooth = self.checkSmoothType(smooth)
        self.rawdata = self.readFile(path)
        self.train_data, self.test_data = self.splitTrainTestandTokenize(5, 0)
        self.vocabulary = self.makeVocabulary()
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
        return self.tokenizeDataset(self.rawdata[test_count:]), self.tokenizeDataset(self.rawdata[0:test_count])

    def makeVocabulary(self):
        vocab = {}
        # for tokens in self.train_data:
        #     for token in tokens:
        #         if 
        return vocab

    def train(self):
        tmodel = {}
        for tokens in self.train_data:
            temp = (['<START>'] * (self.ngram - 1)) + tokens
            for i in range(self.ngram - 1, len(temp)):
                base = ' '.join(temp[i - (self.ngram - 1): i])
                word = temp[i]
                if(base not in tmodel):
                    tmodel[base] = {"<TOTAL_COUNT>": 0}
                if(word != "<TOTAL_COUNT>"):
                    if(word not in tmodel[base]):
                        tmodel[base][word] = 0
                    tmodel[base][word] += 1
                    tmodel[base]["<TOTAL_COUNT>"] += 1
        self.tmodel = tmodel

    def getPerplexity(self, sentence):
        temp = tokenize(sentence.strip())
        temp = (['<START>'] * (self.ngram - 1)) + temp
        for i in range(self.ngram - 1, len(temp)):
            base = ' '.join(temp[i - (self.ngram - 1): i])
            word = temp[i]
            if(base in self.tmodel):
                cbase = self.tmodel[base]["<TOTAL_COUNT>"]
            else:
                cbase = 0
            if(word != "<TOTAL_COUNT>" and cbase > 0 and word in self.tmodel[base]):
                ctotal = self.tmodel[base][word]
            else:
                ctotal = 0
            # pw = 
        return

if(len(sys.argv) == 4):
    lm = LanguageModel(int(sys.argv[1]), sys.argv[2], sys.argv[3])
else:
    print("Invalid number of parameters")