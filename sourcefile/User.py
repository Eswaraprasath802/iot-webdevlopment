import pymongo
from sourcefile.database import databaseconnection
from sourcefile.session import Session
from sourcefile import get_config
from time import time
from random import randint
import json
import bcrypt
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint
from uuid import uuid4
from mongogettersetter import MongoGetterSetter
from sourcefile import hash_password

db=databaseconnection.connection("Eswaraprasath_Iot")

class Usercollection(metaclass=MongoGetterSetter):
  def __int__(self,username):
    self._collection=db.users  # the two line must me like the same varaiable nothing could ne change 2 hours to find the error
    self._filter_query ={
        "$or":[{ "username":username},{"id":username}]
    }
    


class user:
  def __init__(self,id):
    self.connection=Usercollection(id)
    self.id=self.collection.id
    self.username=self.collection.username

  @staticmethod
  def register(username,password,confirm_password,name,email):
    id_=str(uuid4())
    db=databaseconnection.connection("Eswaraprasath_Iot")
    if(password!=confirm_password):
      raise Exception ("The password and confirm password should match")
    else:
      password=password.encode()
      salt=bcrypt.gensalt()
      password=bcrypt.hashpw(password,salt)
      id=db.registers.insert_one({
        "Username":username,
        "Password":password,
        "name":name,
        "Register_time":time(),
         "active":False,
         "Token":randint(1000,10000), 
         "id":id_,
         "email":email
      })
      return id_

  @staticmethod
  def login(username,password):
    db=databaseconnection.connection("Eswaraprasath_Iot")
    info=db.registers.find_one({"Username":username})
    if info:
      # if info.get("Password")==password:
      #   return True
      # else:
      #   raise Exception ("The password is wrong")
      hasedpw=info.get("Password")
      if bcrypt.checkpw(password.encode(),hasedpw):
        sess=Session.register_session(username,request=request)
        return sess._id
      else:
        raise Exception ("The password is wrong")
    else:
      raise Exception("Check The Username and Password")

    