import string
import constants
from stemming.porter2 import stem

class document:
	def __init__(self, rawDoc):
		self.relevant = rawDoc["Relevant"]
		self.url = rawDoc["Url"]

		# list representation of title 
		self.titleWordList = self.__processDoc(rawDoc["Title"])
		# map of all words' positions in title: word->[pos]
		self.titleWordPos = self.__getWordPos(self.titleWordList)

		# list representation of description
		self.descriptionWordList = self.__processDoc(rawDoc["Description"])
		# map of all words' positions in descriptions: word->[pos]
		self.descriptionWordPos = self.__getWordPos(self.descriptionWordList)
		return

	def __str__(self):
		print self.url
		print self.relevant
		print self.titleWordList
		print self.descriptionWordList
		return ""

	def __processDoc(self, textStr):
		# change words to lowercase and remove stopWords
		stopWords = set(constants.stopWord)
		textStr = ' '.join([word.lower() for word in textStr.split() if word.lower() not in stopWords])

		# remove Punctuation
		punctuation = set(string.punctuation)
		textStr = ''.join(char for char in textStr if char not in punctuation)

		# do stemming
		wordList = [stem(word) for word in textStr.split()]
		return wordList

	def __getWordPos(self, wordList):
		wordPos = {}
		for i in range(len(wordList)):
			word = wordList[i]
			if word in wordPos.keys():
				wordPos[word].append(i)
			else:
				wordPos[word] = [i]
		return wordPos

   	def getTF(self):
   		return

   	def getIDF(self):
   		return

   	def getTFIDF(self):
   		return


