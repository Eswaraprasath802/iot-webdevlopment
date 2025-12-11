import json
def get_config(key):
  filepath = "/home/eswaraprasath/iot-webdevlopment/config.json"
  file=open(filepath,"r")
  config=json.loads(file.read())
  if key in config:
    return config[key]
  else:
    raise Exception ("Key is noy found") 
