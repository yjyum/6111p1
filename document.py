import string
import constants
import math
from stemming.porter2 import stem

class document:
	relevant = True			# whether document is relevant
	url = ""				# url of document
	title = ""				# title of document
	noStemTitleWordList = []# list representation of title without stemming
	titleWordList = []		# list representation of processed title
	titleWordPos = {}		# map of all words' positions in title: word->[pos]
	noStemDescriptionWordList = []	# list representation of description without stemming
	descriptionWordList = []# list representation of description
	descriptionWordPos = {}	# map of all words' positions in descriptions: word->[pos]
	descriptionTF={}        # map of all words' frequency in description
	titleTF = {}            # map of all words' frequency in title

	def __init__(self, rawDoc):
		self.relevant = rawDoc["Relevant"]
		self.url = rawDoc["Url"]
		self.title = rawDoc["Title"].lower()

		self.noStemTitleWordList = self.__removeStopwords(rawDoc["Title"])
		self.titleWordList = self.__stem(self.noStemTitleWordList)
		self.titleWordPos = self.__getWordPos(self.titleWordList)

		self.noStemDescriptionWordList = self.__removeStopwords(rawDoc["Description"])
		self.descriptionWordList = self.__stem(self.noStemDescriptionWordList)
		self.descriptionWordPos = self.__getWordPos(self.descriptionWordList)

		self.titleTF, self.descriptionTF = self.getTF()
		return

	def __str__(self):
		print self.url
		print self.relevant
		print self.titleWordList
		print self.descriptionWordList
		return ""

	def __removeStopwords(self, textStr):
		# change words to lowercase and remove stopWords
		stopWords = set(constants.stopWord)
		textStr = ' '.join([word.lower() for word in textStr.split() if word.lower() not in stopWords])

		# remove Punctuation
		punctuation = set(string.punctuation)
		textStr = ''.join(char for char in textStr if char not in punctuation)

		return textStr.split()

	def __stem(self, wordList):
		# do stemming
		return [stem(word) for word in wordList]

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
		titleTF={}
		descriptionTF={}
		for word in self.titleWordPos.keys():
			titleTF[word] = 1+math.log(len(self.titleWordPos[word]))

		for word in self.descriptionWordPos.keys():
			descriptionTF[word] = 1+math.log(len(self.descriptionWordPos[word]))

   		return titleTF,descriptionTF


