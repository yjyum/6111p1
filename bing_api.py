import urllib2
import base64
import json


def search(queryList, accountKey):
    #change blank space in the query into %20
    query = "%20".join(queryList)
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+query+'%27&$top=10&$format=json'

    print "URL: ", bingUrl

    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = json.loads(response.read())

    #title, URL, and description
    result=[]
    for info in content["d"]["results"]:
        temp=info
        result.append(temp)

    '''#print out title, URL, and description
    for info in result:
        print info["Description"]
        print info["Title"]
        print info["Url"]'''

    return result
