from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
from sourcefile.session import Session
from sourcefile.apigroups import API as apigroup
from sourcefile.API import API, APIcollection
from sourcefile.device import API_devices as Device
from sourcefile import get_config
bp=Blueprint('device_api', __name__, url_prefix='/device')

@bp.route('/add/device_api',methods=["POST"])
def add_device():
  if session.get("authenticated") and "name" in request.form and "type" in request.form and "group" in request.form and "remarks" in request.form :
    name=request.form["name"]
    dtype=request.form["type"]
    api=request.form["group"]
    remarks=request.form["remarks"]

    if len(name)<3:
       print("hai")
       return{
      "status":"name is too short"
      },401
      
    if len(remarks)<3:
      return{
      "status":"remarks is toos short"
      },402

    vaild_type=False
    d_type=get_config("device")
    print(dtype)
    for _type in d_type:
      if _type["id"]==dtype:
        vaild_type=True
        break
    # print(vaild_type)
    if vaild_type==False:
        return{
          "Status":"failed",
        },400
    api_key=API(api)
    print("completed the hai")
    if (api_key.is_validy()):
      dev_id=Device.register_device(name,dtype,api,remarks,session.get("username"))
      return{
        "staus":"success",
        "message":dev_id.API_collection.id
      },200
    else:
      return{
      "status":"failed"
      },405
  else:
    return{
      "status":"failed"
      },400