class rocchio:
    def __init__(self):
        self.alpha = 1
        self.beta = 0.75
        self.gamma = 0.15
        self.weight = {}
        return

    def compute(self, queryList, documents):
        relevantDocNum = 0
        for url, doc in documents.iteritems():
            if doc.relevant:
                relevantDocNum = relevantDocNum + 1
        totalDocNum = len(documents)

        for url, doc in documents.iteritems():
            if doc.relevant:
                temp = self.beta/relevantDocNum
            else:
                temp = -self.gamma/(totalDocNum-relevantDocNum)

            for word in doc.titleWordList:
                if word in self.weight.keys():
                    self.weight[word] = self.weight[word] + temp
                else:
                    self.weight[word] = temp

            for word in doc.descriptionWordList:
                if word in self.weight.keys():
                    self.weight[word] = self.weight[word] + temp
                else:
                    self.weight[word] = temp

        for query in queryList:
            if query in self.weight.keys():
                self.weight[query] = self.weight[query] + self.alpha
            else:
                self.weight[query] = self.alpha

        newQuery = ""
        maxScore = float("-inf")
        for term in self.weight.keys():
            if term not in queryList:
                if self.weight[term] > maxScore:
                    newQuery = term
                    maxScore = self.weight[term] 

        print self.weight

        return newQuery
