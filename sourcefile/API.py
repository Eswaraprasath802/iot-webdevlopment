from mongogettersetter import MongoGetterSetter
from sourcefile.database import databaseconnection
from uuid import uuid4
from time import time
db=databaseconnection.connection()
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint

class APIcollection(metaclass=MongoGetterSetter):
    def __init__(self,_id):
        self._collection = db.api_keys
        self._filter_query = {
    '$or': [
        {"id": _id},
        {"device_name": _id}
    ]
}


class API:
  def __init__(self,_id):
    self._id=_id
    self.API_collection=APIcollection(_id)
    return self.API_collection
     
  def is_validy(self):
    vaildity = self.API_collection.vaildity
    print(" all right")
    login_time = self.API_collection.time
    # vaildity = self.API_collection.vaildity
    if vaildity==0:
      return True
    else:
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
      collection=db.groups
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
        "request":request_info
      })
      return id_
    