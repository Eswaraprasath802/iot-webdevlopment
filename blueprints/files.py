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
        file=fs.files.find_one({
            "filename":filename
        })
        return send_file(file,mimetype=file.metadata['content_type'],as_attachment=True,download_name=file.original_filname)
    
    except Exception as e:
        return "file not found",404

@bp.route('/stream/<filename>',methods=['GET'])
def stream_fs(filename):
    db=databaseconnection.connection()
    data=db.fs.files.find_one({
        "filename":filename
    })
    if not data :
        return "File not found",404

    chunk_size=data["chunkSize"]
    total_length=data["length"]
    contenttype=data["metadata"]["content_type"]
    range_header=request.headers.get('Range',None)
    if not range_header:
        start_byte=0
        end_byte=chunk_size-1
    else:
        range_bytes = range_header.split("=")[1]
        range_split = range_bytes.split("-")
        start_byte=int(range_split[0])
        if range_split[1]=="":
            end_byte = total_length- 1
        else:
            end_byte=int(range_split[1])

    end_byte = min(end_byte, total_length - 1)
    start_chunk= start_byte // chunk_size
    end_chunk=end_byte // chunk_size
    def stream():
        for chunk_number in range(start_chunk,end_chunk+1):
            chunk=db.fs.chunks.find_one({
                    "files_id":data["_id"],
                    "n":chunk_number
                })
            start_index = max(0, start_byte - (chunk_number * chunk_size))
            end_index = min(chunk_size, end_byte - (chunk_number * chunk_size) + 1)
            yield chunk['data'][start_index:end_index]

    result=Response(stream(),status=206,mimetype=data["metadata"]['content_type'],direct_passthrough=True)
    result.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start_byte, end_byte,  total_length))
    result.headers.add('Accept-Ranges', 'bytes')
    return result

