from flask import Flask, render_template, session, redirect, url_for, request, Blueprint,Response,send_file
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
        result=Response(file.read(),status=200,mimetype=file.metadata['content_type'])
        print("i am completely fine")
        return result
    
    except Exception as e:
        return "file not found",404

@bp.route('/upload/put', methods=['POST'])
def upload_file_in_put():
    if 'file' in request.files and session['authenticated']:
        files=request.files["file"]
        fs=GridFS(databaseconnection.connection())
        metadata={
            'orginal_filename':files.filename,
            'content_type':mimetypes.guess_type(files.filename)[0]

        }
        filename=str(uuid.uuid4())
        fs.put(files,filename=filename,metadata=metadata,text="jsut for fun",original_filname=files.filename)
        return{
             "filename":files.filename,
             "message": "file uploaded successfully",
            
             "download_url": '/files/get/'+filename
        }
    else:
        return {
            'message':'something went wrong'
            
        },400
    

@bp.route('/get/<filename>',methods=['GET'])
def get_file(filename):
    fs=GridFS(databaseconnection.connection())
    try:
        file=fs.find_one({
            "filename":filename
        })
        return send_file(file,mimetype=file.metadata['content_type'],as_attachment=True,download_name=file.original_filname)
    
    except Exception as e:
        return "file not found",404



    