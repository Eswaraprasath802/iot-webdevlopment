import sys
sys.path.append('/home/eswaraprasath/iot-web/iot-webdevlopment')
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint
import os
import math
from sourcefile import get_config
from sourcefile.User import user
from blueprints import home,api,files,motion,dialog,device,device_api
from sourcefile.API import API


# app=Flask(__name__
basename=get_config("basename")
application=app = Flask(__name__,static_folder="assets",static_url_path=basename)

@app.before_request
def get_token():
    if session.get("type")=='web':
        return
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
      auth_token = auth.split(" ")[1]
      try :
         api=API(auth_token)
         validity=api.is_validy()
         session["authenticated"]=True
         session['username']=api.API_collection.username
         session['type']='api'
         session['sessid']=None
      except Exception as e:
         return {
            "status": "failure",
            "message": "Invalid or missing API key: " + str(e)
         },401
    else:
      session["authenticated"]=False
      if 'username' in session:
         del session["username"]
app.secret_key= get_config("secret_key")
app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)
app.register_blueprint(motion.bp)
app.register_blueprint(dialog.bp)
app.register_blueprint(device.bp)
app.register_blueprint(device_api.bp)



if __name__ == '__main__':
   app.run(host='0.0.0.0',port=7000,debug=True)