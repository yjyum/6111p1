class rocchio:
    def __init__(self):
        self.alpha = 1
        self.beta = 0.75
        self.gamma = 0.15
        self.weight = {}
        return

    def compute(self, queryList, result, relevantResult):
        for r in result:
            for s in r["Title"].split():
                if r["Relevant"]:
                    temp = self.beta/relevantResult
                else:
                    temp = -self.gamma/(len(result)-relevantResult)

                if s in self.weight.keys():
                    self.weight[s] = self.weight[s] + temp
                else:
                    self.weight[s] = temp

            for s in r["Description"].split():
                if r["Relevant"]:
                    temp = self.beta/relevantResult
                else:
                    temp = -self.gamma/(len(result)-relevantResult)

                if s in self.weight.keys():
                    self.weight[s] = self.weight[s] + temp
                else:
                    self.weight[s] = temp

        for s in queryList:
            if s in self.weight.keys():
                self.weight[s] = self.weight[s] + self.alpha
            else:
                self.weight[s] = self.alpha

        newQuery = ""
        maxScore = float("-inf")
        for term in self.weight.keys():
            if term not in queryList:
                if self.weight[term] > maxScore:
                    newQuery = term
                    maxScore = self.weight[term] 

        return newQuery
