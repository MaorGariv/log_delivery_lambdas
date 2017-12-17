from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='cdn_log_shipping',
    KeySchema=[
        {
            'AttributeName': 'Customer',
            'KeyType': 'HASH'  #Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Customer',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

'''
Should also include the following attributes (to be added later)
        {
            'AttributeName': 'BucketArn',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'TargetBucket',
            'AttributeType': 'S'
        },
'''
print("Table status:", table.table_status)