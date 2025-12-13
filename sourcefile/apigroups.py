from mongogettersetter import MongoGetterSetter
from sourcefile.database import databaseconnection
from uuid import uuid4
from time import time
db=databaseconnection.connection()
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint

class APIgroups(metaclass=MongoGetterSetter):
  def __init__(self,_id):
    self._collection=db.api_keys  # the two line must me like the same varaiable nothing could ne change 2 hours to find the w
    self._filter_query ={"id":_id}

class API:
  def __init__(self,_id):
    self._id=_id
    self.API_collection=APIgroups(_id)

  @staticmethod
  def register_group(name,description):
    if session.get("authenticated") is None or session.get("authenticated")==False:
      raise Exception("User not authenticated")
    else:
      collection=db.api_keys
      username=session["username"]
      id_=str(uuid4())
      session_generated=collection.insert_one({
        "id":str(id_),
        "username":username,
         "device_name":name,
         "active":True,
         "description":description,
        "time":time(),#7 days
        "active":True,
  
      })
      return API(id_)
    
  @staticmethod
  def get_all_api_keys():
    collection=db.api_keys
    results=collection.find({})
    return results