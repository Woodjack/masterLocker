import os
import pymongo
from bson.json_util import dumps

def getMONGO():
	mongohq_url = 'mongodb://pull:pull@dharma.mongohq.com:10014/app16815592'
	connection = pymongo.Connection(mongohq_url)
	db = connection.app16815592
	coll = db.locations
	mongoResults = coll.find()
	if mongoResults:
	    results = dumps(mongoResults)
	    return(results)
	else:
	    return('404')