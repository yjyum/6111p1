import operator
from stemming.porter2 import stem

class queryReorder:
	def reorder(self, queryList, documents):
		bigramCount = {}

		# get all bigram from raw titles
		for i in range(len(queryList)):
			w1 = queryList[i]
			for j in range(i+1, len(queryList)):
				w2 = queryList[j]
				bigramCount[(w1, w2)] = 0
				bigramCount[(w2, w1)] = 0

		# calculate frequency of all bigram in related docs
		for url, doc in documents.iteritems():
			if doc.relevant:
				for bigram in bigramCount.keys():
					if doc.title.find(bigram[0] + " " + bigram[1]) != -1:
						bigramCount[bigram] = bigramCount[bigram] + 1

		sorted_bigramCount = sorted(bigramCount.items(), key=operator.itemgetter(1), reverse=True)

		# add bigrams with count more than 0 in decreasing frequency sorder
		temp = {}
		for item in sorted_bigramCount:
			bigram, freq = item[0], item[1]
			if freq == 0:
				break

			# if two words in bigram already added, combine to form 4gram if possible
			if bigram[0] not in queryList and bigram[1] not in queryList:
				b0, b1 = ("", ""), ("", "")
				for nGram in temp.keys():
					if bigram[0] in nGram:
						b0 = nGram
					if bigram[1] in nGram:
						b1 = nGram
				if bo != b1:
					if bigram[0] == b0[1] and bigram[1] == b1[0]:
						temp[(b0[0], b1[1])] = temp[b0] + temp[b1]
					if bigram[0] == b1[1] and bigram[1] == b0[0]:
						temp[(b1[0], b0[1])] = temp[b1] + temp[b0]
			# if one word in bigram already added, add the other to form 3gram if possible
			elif bigram[0] not in queryList:
				for nGram in temp.keys():
					if nGram[1] == bigram[0]:
						temp[(nGram[0], bigram[1])] = temp[nGram] + [bigram[1]]
						del temp[nGram]
						queryList.remove(bigram[1])
						break
			elif bigram[1] not in queryList:
				for nGram in temp.keys():
					if nGram[0] == bigram[1]:
						temp[(bigram[0], nGram[1])] = [bigram[0]] + temp[nGram]
						del temp[nGram]
						queryList.remove(bigram[0])
						break
			# if neither word in bigram added, add the bigram
			else:
				temp[bigram] = [bigram[0], bigram[1]]
				queryList.remove(bigram[0])
				queryList.remove(bigram[1])

		# add left words which are not in any bigram
		newQueryList = []
		for key, value in temp.iteritems():
			newQueryList.extend(value)
		for leftQuery in queryList:
			newQueryList.append(leftQuery)

		return newQueryList
