import json
import hashlib
def get_config(key):
  filepath = "/home/eswaraprasath/iot-webdevlopment/config.json"
  file=open(filepath,"r")
  config=json.loads(file.read())
  if key in config:
    return config[key]
  else:
    raise Exception ("Key is noy found") 


def hash_password(value):
    value = str(value)   # CRITICAL LINE
    hash_object = hashlib.sha256(value.encode("utf-8"))
    return hash_object.hexdigest()


