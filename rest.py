import os
import datetime
import pymongo
from mongodb import db
from bson.json_util import dumps
from bson.json_util import loads
import ast

def getLive(queryList):

	data=[]
	eventsDB = db.events

	for cookie in queryList:
		personinfo = eventsDB.find({'cookie': cookie, {'_id': 0,'date':0,'cookie':0}).sort('date',1).limit(1)
		getResults = dumps(personinfo)

		if getResults != "[]":
			try:
				results = ast.literal_eval(getResults)[0] #this translates getResults as a list, then grabs the first (and only) element
				data.append( results )
			except IndexError:
				print('index error!!!')
		else:
			continue
	if data != []:
	    return( dumps(data) )
	else:
	    return("getLive: No Results" )

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