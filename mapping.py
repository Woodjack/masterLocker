from mongodb import db
from bson.json_util import dumps
from bson.json_util import loads


## This function takes a pymongo .find()
## result and makes it into one single polyline
def makeLineFromPoints(pointsJSON):
	results = {}
	pointsJSON = loads(pointsJSON)
	temp = pointsJSON[0]
	results['name'] = str(temp['name'])
	results['type'] = 'polyline'
	results['points'] = []
	for i in pointsJSON:
		results['points'].append([  float(i['loc']['x']) , float(i['loc']['y']) ])
	return results


def testing():
	mongoResults = coll.find({'name':'Justin'},{'_id':0})[:5] #do a query for justin, only give back 5 results
	if mongoResults:
	    results = dumps(mongoResults) #put into a string
	    print( makeLineFromPoints(results) ) #make it into a line
	else:
	    print('No Results')
