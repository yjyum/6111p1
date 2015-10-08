import sys
import bing_api
from document import *
from rocchio import *

def main(argv):
	# parse input arguments
	accountKey = sys.argv[1]
	precisionTarget = float(sys.argv[2])
	queryList = sys.argv[3].split()

	# map of all returned documents: url->document
	documents = {}

	# loop of getting user feedback and improving results
	while True:
		print "\nParameters:"
		print "Client Key = ", accountKey
		print "Query      = ", ', '.join(queryList)
		print "Precision  = ", precisionTarget

		# retrieve top-10 results from query using Bing API
		result = bing_api.search(queryList, accountKey)

		# print results and getting user-rated relevance
		relevantResult = 0
		totalResult = len(result)

		# exit if fewer than 10 results overall
		if totalResult < 10:
			print "Fewer than 10 results returned, exit"
			break

		print "\nTotal no of results : ", totalResult
		print "Bing Search Results:"
		print "======================"

		for i in range(totalResult):
			print "\nResult ", i+1
			print "["
			print " URL: ", result[i]["Url"]
			print " Title: ", result[i]["Title"]
			print " Summary: ", result[i]["Description"]
			print "]"

			choice = raw_input("Relevant (Y/N)?").lower()
			if choice == "yes" or choice == "y":
				result[i]["Relevant"] = True
				relevantResult = relevantResult + 1
			else:
				result[i]["Relevant"] = False

		# calculate precision
		precision = relevantResult / float(totalResult)
		print precision

		print "======================"
		print "FEEDBACK SUMMARY"
		print "Query ", ', '.join(queryList)
		print "Precision ", precision

		# exit if no relevant results
		if relevantResult == 0:
			print "No relevant results, exit"
			break

		# exit if achieve target precision, append query if not
		if precision >= precisionTarget:
			print "Desired precision reached, done"
			break
		else:
			print "Still below the desired precision of ", precisionTarget
			for r in result:
				doc = document(r)
				documents[r["Url"]] = doc
			queryList = rocchio().compute(queryList, documents)

			# print "Augmenting by", newQuery
			# queryList.append(newQuery)

if __name__ == '__main__':
	main(sys.argv[1:3])