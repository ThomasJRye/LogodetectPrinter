import boto3
import os
from dotenv import load_dotenv

def connect():
    # load environment variables from .env file
    load_dotenv()

    # access specific s3 bucket
    bucket_name = os.getenv('AWS_BUCKET')

    # create an S3 client
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket_name)


    return s3, bucket


def import_logos():
    # load environment variables from .env file
    load_dotenv()

    # access specific s3 bucket
    bucket_name = os.getenv('AWS_BUCKET')
    # create an S3 client
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # create an S3 client
    client = boto3.client('s3')
    # Use the list_objects method to get a list of all files in the directory
    for obj in bucket.objects.filter(Prefix = 'logos'):
        print(obj)
        #s3.Object(bucket, obj.key).download_file(obj.key)
        try :
            print(obj.key)
            client.download_file(bucket_name,  obj.key, '/home/ubuntu/.hkt/logodetect/data/' + obj.key,)
        except Exception as e:
            print(e)
            continue
