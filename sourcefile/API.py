from mongogettersetter import MongoGetterSetter
from sourcefile.database import databaseconnection
from uuid import uuid4
from time import time
db=databaseconnection.connection()
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint
from sourcefile import hash_password

class APIcollection(metaclass=MongoGetterSetter):
    def __init__(self,_id):
        self._collection = db.api_keys
        self._filter_query ={
    '$or': [
        {"id": _id},
        {"hash": _id}
    ]
}

class API:
  def __init__(self,_id):
    self.API_collection=APIcollection(_id)
    try:
      self._id=self.API_collection.id # this line purpose is to check the passed id and the id qquerying from the database are same or not
    except Exception as e:
      raise Exception("Invalid API key")
   
     
  def is_validy(self):
    vaildity=0
    login_time = self.API_collection.time
    # vaildity = self.API_collection.vaildity
    if vaildity==0:
      return self.API_collection.active
    else:
      if self.API_collection.active:
        time_now=time()
        return time_now-login_time < vaildity
    '''
    Types of Sessions
    1. plain - username and password based authentication
    2. api - api key based authentication
    '''

  @staticmethod
  def register_api(session,name,description,remarks,request=request,_type="api"):
    if session.get("authenticated") is None or session.get("authenticated")==False:
      raise Exception("User not authenticated")
    else:
      collection=db.api_keys
      username=session["username"]
      id_=str(uuid4())
      if request is not None:
        request_info={
          "ip_address" : request.headers.get('X-Forwarded-For', request.remote_addr),
          "user_agent" : request.headers.get('User-Agent'),
          "method" : request.method,
          "url" : request.url,
          'headers': dict(request.headers)
        }
      else:
        request_info=None
      session_generated=collection.insert_one({
        "id":str(id_),
        "username":username,
         "device_name":name,
        "device_group":description,
        "remarks":remarks,
        "time":time(),
        "active":True,
        "type":_type,
        "request":request_info,
        "hash":hash_password(id_) 
        # This line is one of the important lines       
        })
      return API(id_)
    
  @staticmethod
  def get_api(session):
    if session.get("authenticated") is None or session.get("authenticated")==False:
      raise Exception("User not authenticated")
    else:
      username=session['username']
      groups=db.api_keys
      result=groups.find({"username":username})
      print(result)
      result = list(result)
      return result

      
    