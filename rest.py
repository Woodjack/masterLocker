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

def updateUserName(data):
	coll = db.users
	coll.update(data)



def getLive():
	data=[]
	eventsDB = db.events
	usersDB = db.users
	query =	eventsDB.distinct('cookie')
	date = datetime.datetime.utcnow() - datetime.timedelta(seconds = 180)
	for cookie in query:
		personinfo = eventsDB.find({'cookie': cookie, "date": { "$gte": date } },{'_id': 0,'date':0,'cookie':0}).sort('date',1).limit(1)
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


def getLiveWithoutMe(cookieID):
	data = getLive()
	data = ast.literal_eval(data) #This turns it into a list, if you want it as a dict, put a [0] in the bound
	print(data)
	print(type(data)) #type is a list





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