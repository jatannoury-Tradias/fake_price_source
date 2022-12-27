from app.controllers.processing.S3_bucket_handler import s3_bucket_controller
from app.config.constants import PRICE_UPDATE_TIME,DEFAULT_FILE_NAME
from app.controllers.responses.stream_processed import stream_processed

def file_name_generator(request_body):
    if "fileName" not in request_body:
        return DEFAULT_FILE_NAME
    elif request_body['fileName'].lower()=="default" or request_body['fileName']=="":
        return DEFAULT_FILE_NAME
    else:
        return request_body['fileName']

async def process_and_stream(websocket,source_type,request_body):
    """
    process input data and calls stream_processed
    Args:
        websocket: websocket object created
        source_type: (fromS3bucket/fromRequest) data source
        request_body: message sent

    Returns: Null

    """
    config=[]
    if source_type=="REQUEST":
        if "payload" not in request_body or request_body['payload']=="" or request_body['payload']==[]:
            config=[{"Warning":"Payload empty"}]
        else:
            config=request_body['payload']
    elif source_type=="BUCKET":
        file_name=file_name_generator(request_body)
        newS3Controller = s3_bucket_controller()
        config = newS3Controller.get_file_from_bucket(file_name) if (source_type=="BUCKET" or source_type not in request_body) else [{"Warning":"Something went wrong"}]
    delta_value=PRICE_UPDATE_TIME if "time_delta" not in request_body or request_body['time_delta']==0 else request_body['time_delta']
    await stream_processed(websocket,config,delta_value)

