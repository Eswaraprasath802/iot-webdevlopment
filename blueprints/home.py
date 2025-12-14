from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.apigroups import API as apigroup
from sourcefile.API import API, APIcollection
from sourcefile import hash_password
bp=Blueprint('home', __name__, url_prefix='/')

@bp.route('/dashboard')
def dashboard():
   print("welcome to dashboard")
   d={
      "authentication":True
   }
   print("testing to dashboard")
   return render_template('dashboard.html',data=session)

@bp.route('/devices')
def devices():
   print("welcome to devices")
   key=API.get_api(session)
   group=apigroup.get_all_api_keys()
   return render_template('devices.html',data=session,key=key,groups=group,hash_password=hash_password)

@bp.route('/row/<hash>',methods=['GET'])
def row(hash):
   group=apigroup.get_all_api_keys()
   # hashing=request.args.get('hash')
   api=API(hash)
   key=api.API_collection._data
   print(key)
   return render_template('api_key/row.html',key=api.API_collection._data,groups=group)

