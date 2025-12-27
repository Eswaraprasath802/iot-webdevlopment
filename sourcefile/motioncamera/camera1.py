from sourcefile.device import API_devices
from sourcefile.database import databaseconnection
from time import time
class Motioncamera(API_devices):
  def __init__(self,_id):
    super().__init__(_id)
    self._type="mcamera"
    self.db=databaseconnection.connection()

  def save_capture(self,file_id,facess):
    self.db.motion_capture.insert_one({
      "file id":file_id,
      "time":time(),
      "device_id":self._id,
      "owner":self.API_collection.username,
      "facess":facess

    })