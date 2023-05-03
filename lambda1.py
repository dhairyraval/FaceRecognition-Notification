# References:
#
# 1. AWS Lambda with Rekognition and DynamoDB
# URL: https://docs.aws.amazon.com/rekognition/latest/dg/stored-video-lambda.html
# Author: AWS
# Date Accessed: April 8, 2023
#
# 2. AWS Lambda with API Gateway
# URL: https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
# Author: AWS
# Date Accessed: April 8, 2023

import boto3
import json
import urllib

dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    print("Records: ",event['Records'])
    key = event['Records'][0]['s3']['object']['key']
    print("Key: ",key)
    
    try:
        # raise Exception("Test to demo Exception during user registration")
        response = rekognition.index_faces(
            Image={"S3Object":{"Bucket": bucket,"Name": key}},
            CollectionId="users"
            )
        
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']
            added = s3.head_object(Bucket=bucket,Key=key)
            pName = added['Metadata']['fullname']
            dynamodb.put_item(TableName='facerecognition',Item={'RekognitionId': {'S': faceId},'FullName': {'S': pName}})

        # print(response)
        
        # Sending Appropriate SNS Message
        snsResponse = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:005711172119:RegisterUser",
            Subject="New User Registered Successfully",
            Message= "Dear Admin\nPlease find this email confirmation of the successful registration of the following user into the face-recognition system\n\tUsername: " + pName
        )

        return response
    except Exception as e:
        
        ret = s3.head_object(Bucket=bucket,Key=key)
        pName = ret['Metadata']['fullname']
        
        snsResponse = sns.publish(
            TopicArn="arn:aws:sns:us-east-1:005711172119:RegisterUser",
            Subject="New User Registration Failed",
            Message= "Dear Admin\nIt is with my deepest regrets that I inform you about the failure in registration of the following user into the face-recognition system\n\tUsername: " + pName +"\n\t" + e
        )
        
        print(e)
        raise e