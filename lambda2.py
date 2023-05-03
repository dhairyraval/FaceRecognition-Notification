import boto3
import json
import base64

def lambda_handler(event, context):
    
    # Instances for Rekognition and DynamoDB (collections)
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
    base64Img = event['imgData']
    imgBytes = base64.b64decode(base64Img)
    
    # Searching for a match of the given image against the collection of images in DynamoDB using Rekognition
    res = rekognition.search_faces_by_image(CollectionId='users',Image={'Bytes':imgBytes})
    
    found = False
    name = "not found - n/a"
    for item in res['FaceMatches']:
        faceData = dynamodb.get_item(
            TableName='facerecognition',  
            Key={'RekognitionId': {'S': item['Face']['FaceId']}}
            )
    
        if 'Item' in faceData:
            name = faceData['Item']['FullName']['S']
            found = True

    if found:
        return json.dumps(name + ' Verified!')
    
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('User could not be verified!')
        }