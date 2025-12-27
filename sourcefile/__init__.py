import json
import hashlib
from datetime import datetime, timezone

def time_ago(timestamp):
    now = datetime.now()
    time_difference = now - datetime.fromtimestamp(timestamp)

    # Calculate days, hours, and minutes
    days = time_difference.days
    seconds = time_difference.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Determine the appropriate time unit to display
    if days > 0:
        return f"{days} days ago"
    elif hours > 0:
        return f"{hours} hours ago"
    elif minutes > 0:
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def get_config(key):
  filepath = "/home/eswaraprasath/iot-web/iot-webdevlopment/config.json"
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

def mask(string,length=6):
   hash=string[:length]
   star='**'
   return star+hash
   



