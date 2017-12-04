import urllib
import boto3
import ast
import json
import re
print('Loading function')

def get_folder_name(path):
    pattern = None
    if 'akamai' in path:
        pattern = re.search('archive/akamai/([0-9A-Za-z-]+)/*',path)
    elif 'fastly' in path:
        pattern = re.search('archive/fastly/[^\b]+/[^\b]+/([0-9A-Za-z-]+)/*',path)
    elif 'cf' in path:
        pattern = re.search('archive/cf/([a-z0-9-]+)/*',path)
    else:
        print "No pattern was found for {}. Exiting..".format(path)
        return None
    return pattern.group(1)


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    print event
    file_key = event['Records'][0]['s3']['object']['key']
    if file_key.endswith('/'): # folder creation
        print "No need to copy folders. Exiting"
        return
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    folder_name = get_folder_name(file_key)
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    table = dynamodb.Table('BucketDetails')
    db_response = table.get_item(Key={'Customer':folder_name})
    target_bucket = db_response['Item']['TargetBucket']
    print db_response
    key = file_key
    copy_source = {'Bucket':source_bucket, 'Key':key}
    print "Copying {} from bucket {} to bucket {} ...".format(key, source_bucket, target_bucket)
    s3.copy_object(Bucket=target_bucket, Key=key, CopySource=copy_source, ACL = 'bucket-owner-full-control')