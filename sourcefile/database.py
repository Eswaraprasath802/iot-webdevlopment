from pymongo import MongoClient
from sourcefile import get_config
class databaseconnection:
  @staticmethod
  def connection(database=None):
    client = MongoClient(get_config("mongodb_connection"))
    if database is None: 
      return client.Eswaraprasath_Iot
    else:
      return client[database]
