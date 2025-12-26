from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
from sourcefile.session import Session
from sourcefile.apigroups import API as apigroup
from sourcefile.API import API, APIcollection


bp=Blueprint('api', __name__, url_prefix='/api/v1')

@bp.route('/', methods=['POST'])
def register():
   if "username" in request.form and "password" in request.form and "confirm_password" in request.form  and "name" in request.form and "email" in request.form:
      username=request.form["username"]
      password=request.form["password"]
      confirm_password=request.form["confirm_password"]
      fullname=request.form["name"]
      email=request.form["email"]
      try:
         user.register(username,password,confirm_password,fullname,email)
         return {
            "status": "success",
            "message": "User registered successfully"
         },201
      except Exception as e:
         return {
            "status": "failure",
            "message": "Registration failed: " + str(e)
         },400
   else:
      return {
         "status": "failure",
         "message": "Username, password or confirm password not provided"
      },400

@bp.route('/auth',methods=['POST'])
def authenticate():
   if session.get("authenticated"):
      sess=Session(session['sessid'])
      if sess.is_validy():
         return {
            "status": "success",
            "message": "Already authenticated"
         },202
      else:
         session["authenticated"]=False
         sess.session_collection.active=False
         return {
            "status": "False",
            "message": "session expired"
         },401

   else:
      if "username" in request.form and "password" in request.form: 
         username=request.form["username"]
         password=request.form["password"]
         try:
            sessid=user.login(username,password)
            session["authenticated"]=True
            session["username"]=username
            session["sessid"]=sessid
            if redirect in request.form and request.form["redirect"]==True:
               return redirect(url_for('home.dashboard'))
            else:
               return {
               "message":"successfully authenticated",
               "authendicated":True
            },200
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

@bp.route('/generate/api/key', methods=['POST'])
def generate_api_key():
   name=request.form["name"]
   description=request.form["description"]
   remarks=request.form["remarks"]
   if session.get("authenticated"):
      a=API.register_api(session,name,description,remarks)
      return {
         "status": "success",
         "message": "API key generated successfully",
         "key": a.API_collection.id,
         "hash":a.API_collection.hash
      },201
   else:
      pass

@bp.route('/get/api/group', methods=['POST'])
def get_api_group():
   name=request.form["name"]
   description=request.form["description"]
   apigroup.register_group(name,description)
   return {
         "status": "success",
         "message": "API group registered successfully"
      },201
   return {
         "status": "failure",
         "message": "User not authenticated"
      },401
      