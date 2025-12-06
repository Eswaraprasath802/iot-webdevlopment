from pymongo import MongoClient

client = MongoClient("mongodb://Eswaraprasath:CH3COONA..@mongodb.selfmade.ninja:27017/?authSource=users")
db = client.Eswaraprasath_Iot

db.users.update_one({"area": "8050"},{"$set":{"bedrooms":'9'}})
result=db.users.find_one({"area": "8050"})
print(result)
