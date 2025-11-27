from flask import Flask,redirect,url_for,request,render_template
import os
import math
from sourcefile import get_config
basename=get_config("basename")
app = Flask(__name__,static_folder="assets",static_url_path=basename)

@app.route(basename+'/dashboard')
def welcome():
   d={
      "authentication":True
   }
   return render_template('dashboard.html',data=d)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=7000,debug=True)