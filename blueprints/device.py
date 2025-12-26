from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
from sourcefile.User import user
from sourcefile.session import Session
from sourcefile.apigroups import API as apigroup
from sourcefile.API import API, APIcollection
from sourcefile import get_config
from sourcefile.device import API_devices
bp=Blueprint('device', __name__, url_prefix='/')

@bp.route('/device')
def device():
  return render_template('device.html',data=session,devices=API_devices.get_all_api_keys_devices())

@bp.route('/add/device')
def add():
  return render_template('devices/add.html',data=session,apis=list(API.get_api(session,True)),dtypes=get_config("device"))

@bp.route('/mcamera/<id>')
def mcamera(id):
  pass