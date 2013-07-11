import pymongo

mongohq_url = 'mongodb://rest:service@dharma.mongohq.com:10014/app16815592'
connection = pymongo.Connection(mongohq_url)
db = connection.app16815592