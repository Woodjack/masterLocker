from mongodb import db
from bson.json_util import dumps
from bson.json_util import loads

def makeLineFromPoints(pointsJSON):
	
	results = {}
	pointsJSON = loads(pointsJSON)
	temp = pointsJSON[0]
	results['name'] = temp['name']
	results['type'] = 'polyline'
	results['points'] = []
	for i in pointsJSON:
		results['points'].append(  [ i['loc']['x'], i['loc']['y']] )
	print results



coll = db.events
mongoResults = coll.find({'name':'Justin'},{'_id':0})[:5]
if mongoResults:
    results = dumps(mongoResults)
    makeLineFromPoints(results)
else:
    print('No Results')
