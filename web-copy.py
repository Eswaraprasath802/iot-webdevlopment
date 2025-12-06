from flask import Flask,redirect,url_for,request,render_template
import os
import math

app = Flask(__name__)
basename='/iotweb'
#In the above line we use /iotweb when we serach in the localhost with localhost:7000/iot/ it give error To 
# Resolve this we use /iotweb/ in the above line so we can search both /iotweb and /iotweb/ 
@app.route(basename+"/ht")
def welcome():
   d={
      "name":"Eswaraprasath",
      "he":"you are in our web",
      "avatar":"https://gitlab.com/uploads/-/system/user/avatar/742684/avatar.png?width=800"
      
   }
   return render_template('bootstrap.html',data=d)

@app.route(basename+"/dashboard")
def dashboard():
   return render_template('dash.html')
   
@app.route(basename+'/hai')
def hello_world():
   return 'welcome Eswaraprasath'

@app.route(basename+'/welcome')
def whoami():
   return os.popen("whoami").read()


@app.route(basename+'/we'+'/<guest>')
def wow(guest):
   return 'Welcome to First web Application of Eswaraprasath as the guest {}'.format(guest)
# app.add_url_rule('/', 'wow', wow)


#url building to redirect the internet protocal
@app.route(basename+'/<adminname>')
def url_building(adminname):
   if adminname=="Eswaraprasath":
      return redirect(url_for('hello_world'))
   else:
      return redirect(url_for('wow',guest=adminname))

@app.route(basename)
def cpuinformarmation():
   return "<pre>"+os.popen("cat /proc/cpuinfo").read()+"</pre>"

@app.route(basename+'/hello',methods=['GET','POST'])
def welcomeworld():
   return {"result":(math.sqrt(int(request.form['num'])))}


#we can use <Datatype:Variable_name>
# @app.route(basename+'/<stringname>')
# def variablename(stringname):
#    return 'hello {}' .format(stringname)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=7000,debug=True)