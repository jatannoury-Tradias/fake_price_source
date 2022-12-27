import boto3
import json

from app.models.exceptions.exceptions import InvalidFileName
from app.config.constants import BUCKET_NAME,AWS_CONFIG
class s3_bucket_controller:
    def __init__(self):
        """
        Function responsible to establish the connection with Amazon S3
        """
        self.s3=boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=AWS_CONFIG['aws_access_key_id'],
    aws_secret_access_key=AWS_CONFIG['aws_secret_access_key']
)

    def get_file_from_bucket(self,file_name):
        """
        Function responsible for searching through Amazon S3 for a file given specific file name
        :param file_name:str
        :return: array of objects
        """
        for bucket in self.s3.Bucket(BUCKET_NAME).objects.filter(Prefix=''):
            if file_name in str(bucket.key) :
                print("file_name:",file_name,",bucket_key",bucket.key)
                return json.loads(self.s3.Bucket(BUCKET_NAME).Object(str(bucket.key)).get()['Body'].read().decode('utf-8'))
        InvalidFileName(f"No file named {file_name} found inside S3 bucket-{BUCKET_NAME}")


