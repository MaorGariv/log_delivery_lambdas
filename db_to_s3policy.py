import boto3
import json
import os

def lambda_handler(event, context):
    print event
    if not event['Records'][0]['dynamodb'].has_key('NewImage'):
        print " No new record added. Exiting..."
        return
    target_bucket_arn = str(event['Records'][0]['dynamodb']['NewImage']['BucketArn']['S'])
    print target_bucket_arn
    target_bucket_arn += '/*'
    s3_copy_policy_arn = os.environ['POLICY_ARN']
    iam = boto3.client('iam')
    old_policy = iam.get_policy(PolicyArn = s3_copy_policy_arn)
    old_policy_version = old_policy['Policy']['DefaultVersionId']
    print "Old policy version to delete {}".format(old_policy_version)
    policy_document = iam.get_policy_version(PolicyArn = s3_copy_policy_arn,VersionId = old_policy_version)['PolicyVersion']['Document']
    print "Old Policy - "
    print policy_document
    for statement in policy_document['Statement']:
        if 's3:PutObject' in statement['Action']:
            if type(statement['Resource']) is not list: # only 1 bucket listed
                statement['Resource'] = [statement['Resource'], target_bucket_arn]
            else:
                statement['Resource'].append(target_bucket_arn)
                print statement
            break
    
    new_policy = iam.create_policy_version(PolicyArn = s3_copy_policy_arn,PolicyDocument = json.dumps(policy_document),SetAsDefault = True)
    new_policy_version = new_policy['PolicyVersion']['VersionId']
    iam.delete_policy_version(PolicyArn = s3_copy_policy_arn,VersionId=old_policy_version)
    print "New Policy - "
    print iam.get_policy_version(PolicyArn = s3_copy_policy_arn,VersionId = new_policy_version)['PolicyVersion']['Document']
    return