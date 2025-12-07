from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
bp=Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/auth',methods=['POST'])
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
         print("hai")
         print(username)
         print(password)
         try:
            print("hai")
            user.login(username,password)
            session["authenticated"]=True
            print("hello")
            return redirect(url_for('home.dashboard'))
         except Exception as e:  
             return {
                  "status": "some issue",
                  "message": "Login denied: " + str(e)
            },401
      else:
         return {
               "status": "Failure in username",
               "message": "Username or password not provided"
            },400
@bp.route('/deauth')
def deauthenticate():
   if session.get("authenticated"):
      session["authenticated"]=False
   return {
      "status": "success",
      "message": "Deauthenticated successfully" },200