import sys
sys.path.append('/home/eswaraprasath/iot-web/iot-webdevlopment')
from flask import Flask,redirect,url_for,request,render_template,session,Blueprint
import os
import math
from sourcefile import get_config
from sourcefile.User import user
from blueprints import home,api,files,motion


# app=Flask(__name__
basename=get_config("basename")
application=app = Flask(__name__,static_folder="assets",static_url_path=basename)
app.secret_key= get_config("secret_key")
app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)
app.register_blueprint(motion.bp)





if __name__ == '__main__':
   app.run(host='0.0.0.0',port=7000,debug=True)