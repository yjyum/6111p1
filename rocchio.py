import math
from stemming.porter2 import stem
import operator

class rocchio:
    def __init__(self):
        self.alpha = 1
        self.beta = 0.75
        self.gamma = 0.15
        self.weight = {}
        self.titleidf = {}
        self.descriptionidf = {}
        return

    # compute new query using rocchio algorithms
    def compute(self, queryList, documents):
        relevantDocNum = 0
        for url, doc in documents.iteritems():
            if doc.relevant:
                relevantDocNum = relevantDocNum + 1
        totalDocNum = len(documents)

        #compute idf
        for url, doc in documents.iteritems():
            for word in doc.titleTF.keys():
                addToMap(self.titleidf, word, 1)
            for word in self.titleidf.keys():
                self.titleidf[word]=math.log(len(documents)/self.titleidf[word])
            for word in doc.descriptionTF.keys():
                addToMap(self.descriptionidf, word, 1)
            for word in self.descriptionidf.keys():
                self.descriptionidf[word]=math.log(len(documents)/self.descriptionidf[word])

        for url, doc in documents.iteritems():
            if doc.relevant:
                temp = self.beta/relevantDocNum
            else:
                temp = -self.gamma/(totalDocNum-relevantDocNum)

            for word in doc.titleTF.keys():
                addToMap(self.weight, word, temp*(doc.titleTF[word]*self.titleidf[word]))

            for word in doc.descriptionTF.keys():
                addToMap(self.weight, word, temp*(doc.descriptionTF[word]*self.descriptionidf[word]))

        for query in queryList:
            addToMap(self.weight, query, self.alpha)
            # delete similar words of query generated after stemming
            if stem(query)!=query and stem(query) in self.weight.keys():
                self.weight[query] = self.weight[query]+self.weight[stem(query)]
                del self.weight[stem(query)]
        # debug
        # print sorted(self.weight.items(), key=operator.itemgetter(1))

        # find one new query which is of the max weight
        newQuery = ""
        maxScore = float("-inf")
        for term in self.weight.keys():
            if term not in queryList:
                if self.weight[term] > maxScore:
                    newQuery = term
                    maxScore = self.weight[term] 

        # change new query from root to most frequect form in docs
        oriQuery = {}
        for url, doc in documents.iteritems():
            if doc.relevant:
                if newQuery in doc.titleWordPos.keys():
                    for pos in doc.titleWordPos[newQuery]:
                        addToMap(oriQuery, doc.noStemTitleWordList[pos], 1)
                if newQuery in doc.descriptionWordPos.keys():
                    for pos in doc.descriptionWordPos[newQuery]:
                        addToMap(oriQuery, doc.noStemDescriptionWordList[pos], 1)
        newQuery = max(oriQuery.iteritems(), key=operator.itemgetter(1))[0]

        return newQuery

def addToMap(map, key, value):
    if key in map.keys():
        map[key] += value
    else:
        map[key] = value
