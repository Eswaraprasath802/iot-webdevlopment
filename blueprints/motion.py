from flask import Flask, render_template, session, redirect, url_for, request, Blueprint,Response,send_file
from gridfs import GridFSBucket
from sourcefile.database import databaseconnection
import mimetypes
import uuid
from sourcefile.motioncamera.camera1 import Motioncamera
from sourcefile.API import API
bp=Blueprint('motion', __name__, url_prefix='/motion')

@bp.route('/capture', methods=['POST'])
def motion_capture():
    if 'file' in request.files and session['authenticated']:
        auth = request.headers.get("Authorization")
        if auth:
           auth_token = auth.split(" ")[1]
           api=API(auth_token)
           device=api.get_devices()
           device_id=device['id']
           files=request.files["file"]
           fs=GridFSBucket(databaseconnection.connection())
           metadata={
            'orginal_filename':files.filename,
            'content_type':mimetypes.guess_type(files.filename)[0],
            'device_id':device_id
            

        }
           filename=str(uuid.uuid4())
           file_id= fs.upload_from_stream(filename,files,metadata=metadata)
           mc=Motioncamera(device_id)
           facess={
            "filename":files.filename,
            "message": "file uploaded successfully",
            
            "download_url": '/files/download/'+filename
        }
           mc.save_capture(file_id,facess)
           return facess,200
        else:
          return {
            'message':'something went wrong'

                },400