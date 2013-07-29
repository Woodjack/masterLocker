import pymongo

try:
	connection = pymongo.Connection('localhost')
except:
	connection = pymongo.Connection('mongodb://rest:service@dharma.mongohq.com:10014/app16815592')

db = connection.app16815592