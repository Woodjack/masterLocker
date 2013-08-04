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

def getLive():
	data=[]
	coll = db.events
	query = coll.distinct('cookie')
	date = datetime.datetime.utcnow() - datetime.timedelta(seconds = 180)
	for person in query:
		personinfo = coll.find({'cookie': cookie, "date": { "$gte": date } },{'_id': 0,'date':0,'cookie':0}).sort('date',1).limit(1)
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


def getLiveWithoutMe(currentUserCookie):
	data=[]
	coll = db.events
	date = datetime.datetime.utcnow() - datetime.timedelta(seconds = 180)
	personinfo = coll.find({"date": { "$gte": date } },{'_id': 0,'date':0,'cookie':0})
	uniqueCookies = personinfo.distinct('cookie')
	for cookie in uniqueCookies:
		results = dumps(personinfo)
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

def dumpallpoints():
	data=[]
	coll = db.events
	for point in db.events.find():
		data.append( point )
	if data:
		return( dumps(data) )
	else:
		return( 'No Results' )