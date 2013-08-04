import os
import datetime
import pymongo
from mongodb import db
from bson.json_util import dumps
from bson.json_util import loads
import ast

def getMONGO():
	coll = db.events
	mongoResults = coll.find({},{'_id':0})
	if mongoResults:
	    results = dumps(mongoResults)
	    return(results)
	else:
	    return('No Results')

def postNewUser(data):
	coll = db.users
	coll.insert(data)
	return("Successful mongodb upload bitches!!! ")

def getLiveMONGO():
	data=[]
	coll = db.events
	query = coll.distinct('name')
	date = datetime.datetime.utcnow() - datetime.timedelta(seconds = 180)
	for person in query:
		personinfo = coll.find({'name': person, "date": { "$gte": date } },{'_id': 0}).sort('date',1).limit(1)
		getResults = dumps(personinfo)
		if getResults != "[]":
			try:
				data.append( ast.literal_eval(getResults)[0] )
			except IndexError:
				print('index error!!!')
		else:
			continue
	if data != []:
	    return( dumps(data) )
	else:
	    return("     No results" )

def getCurrentMONGO():
	data=[]
	coll = db.events	
	query = coll.distinct('name')
	for person in query:
		personinfo = coll.find({'name': person},{'_id': 0}).sort('date',1).limit(1)
		getResults = dumps(personinfo)
		data.append( ast.literal_eval(getResults)[0] )
	if data:
	    return( dumps(data) )
	else:
	    return( 'No Results' )

def postLocation(newLocation):
	coll = db.events
	coll.insert(newLocation)
	return("Successful mongodb upload bitches!!!   " + str(newLocation))

def dumpallpoints():
	data=[]
	coll = db.events
	for point in db.events.find():
		data.append( point )

	if data:
		return( dumps(data) )
	else:
		return( 'No Results' )