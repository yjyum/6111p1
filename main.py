import sys
import bing_api

def main(argv):
	# parse input arguments
	accountKey = sys.argv[1]
	precisionTarget = float(sys.argv[2])
	queryList = sys.argv[3].split()

	print "Parameters:"
	print "Client Key = ", accountKey
	print "Query      = ", sys.argv[3]
	print "Precision  = ", precisionTarget

	# loop of getting user feedback and improving results
	while True:
		# retrieve top-10 results from query using Bing API
		result = bing_api.search(queryList, accountKey)

		# print results and getting user-rated relevance
		relevantResult = 0
		totalResult = len(result)

		# exit if fewer than 10 results overall
		if totalResult < 10:
			print "Fewer than 10 results returned, exit"
			break

		print "Total no of results : ", totalResult
		print "Bing Search Results:"
		print "======================"

		for i in range(totalResult):
			print "Result ", i+1
			print "["
			print " URL: ", result[i]["Url"]
			print " Title: ", result[i]["Title"]
			print " Summary: ", result[i]["Description"]
			print "]"

			print ""
			choice = raw_input("Relevant (Y/N)?").lower()
			print choice
			if choice == "yes" or choice == "y":
				relevantResult = relevantResult + 1

		# calculate precision
		precision = relevantResult / float(totalResult)
		print precision

		print "======================"
		print "FEEDBACK SUMMARY"
		print "Query ", sys.argv[3]
		print "Precision ", precision

		# exit if no relevant results
		if relevantResult < 10:
			print "No relevant results, exit"
			break

		# exit if achieve target precision, append query if not
		if precision >= precisionTarget:
			print "Desired precision reached, done"
			break
		else:
			print "Still below the desired precision of ", precisionTarget

if __name__ == '__main__':
	main(sys.argv[1:3])