from mongogettersetter import MongoGetterSetter
from sourcefile.database import databaseconnection
from uuid import uuid4
from time import time
from sourcefile.API import API, APIcollection
db=databaseconnection.connection()
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint

class APIdevices(metaclass=MongoGetterSetter):
  def __init__(self,_id):
    self._collection=db.devices  # the two line must me like the same varaiable nothing could ne change 2 hours to find the w
    self._filter_query ={
    '$or': [
        {"id": _id},
    ]
}

class API_devices:
  def __init__(self,_id):
    self.API_collection=APIdevices(_id)
    self._id=str(self.API_collection.id)

  def delete(self):
    api=API(self.API_collection.api)
    api.API_collection.linked_device=None
    self.API_collection.delete()

  @staticmethod
  def register_device(name,dtype,api,remarks,username):
    if session.get("authenticated") is None or session.get("authenticated")==False:
      raise Exception("User not authenticated")
    else:
      collection=db.devices
      username=session["username"]
      id_=str(uuid4())

      #link the device
      key=API(api)
      key.API_collection.linked_device=id_
      session_generated=collection.insert_one({
        "id":str(id_),
        "username":username,
         "device_name":name,
         "active":True,
         "dtype":dtype,
         "api":api,
         "remarks":remarks,
        "time":time(),#7 days
        "active":True,
        "group":key.API_collection.device_group,
        "linked_device":None
  
      })
      return API_devices(id_)
    
  @staticmethod
  def get_all_api_keys_devices():
    collection=db.devices
    results=collection.find({})
    results = list(results)
    return results