from flask import Flask, render_template, session, redirect, url_for, request, Blueprint
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
   return render_template('devices.html',data=session)

