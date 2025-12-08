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
        end_byte=int(range_split[1])

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




    


    