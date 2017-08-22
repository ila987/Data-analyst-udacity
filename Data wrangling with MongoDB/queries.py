#this code runs some queries over the OpenStreet data loaded in the MongoDB database


from pymongo import MongoClient
from pprint import pprint
import pymongo

client=MongoClient("localhost", 27017)

# Use shortcut to access the database
db = client.OpenStreet

# Use shortcut to access the collection
coll = db.Milan

# Number of documents
print "Number of documents"                                                
print  coll.find().count()

                                              
# Number of nodes
print "Number of nodes"
print coll.find({"type": "node"}).count()

                                                
# Number of ways
print "Number of ways"
print coll.find({"type": "way"}).count()                               


# Number of unique users
print "Number of unique users"                                            
print len(coll.distinct("created.user"))

                                                
# Top 1 contributing user
print "Most contributing user"                                                
aggr =  coll.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":1}])
pprint(list(aggr))

#Find amenities 
print "Count of amenities in the data"
aggr = coll.aggregate( [{"$group":{"_id": "$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}])
pprint(list(aggr))

#Find all restaurant in Milan 
print "Count of different cuisines in resto in Milan city"
aggr = coll.aggregate( [{"$match":{"address.city":"Milano", 
                                  "amenity":"restaurant"}},
                       {"$group":{"_id": "$cuisine", "count":{"$sum":1}}}, {"$sort":{"count":-1}}])
pprint(list(aggr))

#Count opening hours 
print "Check how many times opening hours are there"
print len(coll.distinct("opening_hours"))
