import os
import datetime
import pymongo
from mongodbconf import db
from bson.json_util import dumps
from bson.json_util import loads
import ast
from urlparse import urlparse, parse_qs  #url parsing for query


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
	for person in query:
		personinfo = coll.find({'name': person},{'_id': 0}).sort('date',1).limit(1)
		getResults = dumps(personinfo)
		data.append( ast.literal_eval(getResults)[0] )
	if data:
	    return( dumps(data) )
	else:
	    return( 'No Results' )



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
