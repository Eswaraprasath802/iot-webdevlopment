import pymongo
from sourcefile.database import databaseconnection
from sourcefile import get_config
from time import time
from random import randint
import json
import bcrypt

class user:
  def __init__(self,id):
    db=databaseconnection.connection("Eswaraprasath_Iot")

  @staticmethod
  def register(username,password,confirm_password):
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
        "Register_time":time(),
         "active":False,
         "Token":randint(1000,10000)
      })

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
        return True
      else:
        raise Exception ("The password is wrong")
    else:
      raise Exception("Check The Username and Password")

    