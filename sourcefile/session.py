from mongogettersetter import MongoGetterSetter
from sourcefile.database import databaseconnection
from uuid import uuid4
from time import time
db=databaseconnection.connection()

class Sessioncollection(metaclass=MongoGetterSetter):
  def __init__(self,_id):
    self._collection=db.sessions  # the two line must me like the same varaiable nothing could ne change 2 hours to find the w
    self._filter_query ={"id":_id}

class Session:
  def __init__(self,_id):
    self._id=_id
    self.session_collection=Sessioncollection(_id)
     
  def is_validy(self):
    vaildity = self.session_collection.vaildity
    print(" all right")
    login_time = self.session_collection.time
    # vaildity = self.session_collection.vaildity

    time_now=time()
    return time_now-login_time < vaildity
    '''
    Types of Sessions
    1. plain - username and password based authentication
    2. api - api key based authentication
    '''

  @staticmethod
  def register_session(username,request,vaildity=604800,_type="plain"):
    collection=db.sessions
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
      "time":time(),
      "vaildity":vaildity, #7 days
      "active":True,
      "type":_type,
      "request":request_info
    })
    return Session(id_)
  