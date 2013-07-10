import os
import pymongo
from bson.json_util import dumps
from urlparse import urlparse, parse_qs  #url parsing for query

mongohq_url = 'mongodb://pull:pull@dharma.mongohq.com:10014/app16815592'
connection = pymongo.Connection(mongohq_url)
db = connection.app16815592

def getMONGO():
	coll = db.locations
	mongoResults = coll.find({},{'_id':0})
	if mongoResults:
	    results = dumps(mongoResults)
	    return(results)
	else:
	    return('No Results')

	    

def pushLocation(urlQuery):
	coll = db.locations
	data = parse_qs(urlparse(urlQuery).query)
	jsonLocation = {}
	
	#coll.insert(jsonLocation)
	return(data)
