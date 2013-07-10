import os
import datetime
import pymongo
from bson.json_util import dumps
from urlparse import urlparse, parse_qs  #url parsing for query

mongohq_url = 'mongodb://rest:service@dharma.mongohq.com:10014/app16815592'
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



def getCurrentMONGO():
	coll = db.locations	
	queryLimit = coll.find().distinct('name')
	mongoResults = coll.find({},{'_id':0}).sort({'date',1).limit(1)
	if mongoResults:
	    results = dumps(mongoResults)
	    return(results)
	else:
	    return('No Results')


def getTailsMONGO():
	coll = db.locations
	mongoResults = coll.find({},{'_id':0})
	if mongoResults:
	    results = dumps(mongoResults)
	    return(results)
	else:
	    return('No Results')




def postLocation(newLocation):
	coll = db.locations
	newLocation['date'] = datetime.datetime.utcnow()
	coll.insert(newLocation)
	return("Successful mongodb upload bitches!!! ")
