from flask import Flask, render_template, session, redirect, url_for, request, Blueprint,Response,send_file
from gridfs import GridFSBucket
from sourcefile.database import databaseconnection
import mimetypes
import uuid
bp=Blueprint('motion', __name__, url_prefix='/motion')

@bp.route('/capture', methods=['POST'])
def motion_capture():
    if 'file' in request.files and session['authenticated']:
        files=request.files["file"]
        fs=GridFSBucket(databaseconnection.connection())
        metadata={
            'orginal_filename':files.filename,
            'content_type':mimetypes.guess_type(files.filename)[0]

        }
        filename=str(uuid.uuid4())
        fs.upload_from_stream(filename,files,metadata=metadata)
        return{
             "filename":files.filename,
             "message": "file uploaded successfully",
            
             "download_url": '/files/download/'+filename
        }
    else:
        return {
            'message':'something went wrong'
            
        },400