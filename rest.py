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
	data=[]
	coll = db.locations	
	query = coll.distinct('name')
	print(query)
	for person in query:
		personinfo = coll.find({'name': person},{'_id': 0}).sort('date',1).limit(1)
		results = dumps(personinfo)
		data.append(results)

	print(data)
	if data:
	    return(dumps(data))
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
