import string
import constants
from stemming.porter2 import stem

class document:
	relevant = True			# whether document is relevant
	url = ""				# url of document
	titleWordList = []		# list representation of title
	titleWordPos = {}		# map of all words' positions in title: word->[pos]
	descriptionWordList = []# list representation of description
	descriptionWordPos = {}	# map of all words' positions in descriptions: word->[pos]

	def __init__(self, rawDoc):
		self.relevant = rawDoc["Relevant"]
		self.url = rawDoc["Url"]

		self.titleWordList = self.__processDoc(rawDoc["Title"])
		self.titleWordPos = self.__getWordPos(self.titleWordList)

		self.descriptionWordList = self.__processDoc(rawDoc["Description"])
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

		# no stemming
		# return textStr.split()

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


