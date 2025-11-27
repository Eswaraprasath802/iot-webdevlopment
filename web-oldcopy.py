from flask import Flask,redirect,url_for,request,render_template,session
import os
import math
from sourcefile import get_config
from sourcefile.User import user
basename=get_config("basename")
app = Flask(__name__,static_folder="assets",static_url_path=basename)
app.secret_key= get_config("secret_key")

@app.route(basename+'/dashboard')
def dashboard():
   print("welcome to dashboard")
   d={
      "authentication":True
   }
   print("testing to dashboard")
   return render_template('dashboard.html',data=session)

@app.route(basename+'/auth',methods=['POST'])
def authenticate():
   if session.get("authenticated"):
      return {
         "status": "success",
         "message": "Already authenticated"
      },202
   else:
      if "username" in request.form and "password" in request.form: 
         username=request.form["username"]
         password=request.form["password"]
         try:
            user.login(username,password)
            session["authenticated"]=True
            print("hello")
            return redirect(url_for('dashboard'))
         except Exception as e:  
             return {
                  "status": "Failure",
                  "message": "Login denied: " + str(e)
            },401
      else:
         return {
               "status": "Failure",
               "message": "Username or password not provided"
            },400
@app.route(basename+'/deauth')
def deauthenticate():
   if session.get("authenticated"):
      session["authenticated"]=False
   return {
      "status": "success",
      "message": "Deauthenticated successfully" },200

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=7000,debug=True)