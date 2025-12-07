from flask import Flask, render_template, session, redirect, url_for, request, Blueprint,Response
from gridfs import GridFS,GridFSBucket
from sourcefile.database import databaseconnection
import mimetypes
import uuid
bp=Blueprint('files', __name__, url_prefix='/files')

@bp.route('/upload/bucket', methods=['POST'])
def upload_file():
    print("hai")
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
             #check the url of of https://dashboard.selfmade.technology/files/download/65886623-226a-4888-9318-334e76c67146
             "download_url": '/files/download/'+filename
        }
    else:
        return {
            'message':'something went wrong'
            
        },400
    
@bp.route('/download/<filename>',methods=['GET'])

def download_file(filename):
    fs=GridFSBucket(databaseconnection.connection())
    try:
        file=fs.open_download_stream_by_name(filename)
        result=Response(file.read(),mimetype=file.metadata['content_type'])
        return result
    
    except Exception as e:
        return "file not found",404

    
