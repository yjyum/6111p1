class document:
    def __init__(self):
        self.tf = {}
        self.idf ={}


    def rmstopwords(self,result):
        for r in result:
            for s in result["Title"]:
