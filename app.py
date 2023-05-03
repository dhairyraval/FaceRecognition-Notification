# References:
# 
# 1. Making PUT requests in Python
# URL: https://www.geeksforgeeks.org/put-method-python-requests/
# Author: GeeksForGeeks
# Date Accessed: April 8, 2023


import requests
import io
import json
import base64
from PIL import Image

bucketName = 'users-facedata'
subFolder = 'index'


# Register Function used to register a new user
def register():
    print("Registering new user\n")
    print("Enter the user's full name:")
    username = input()
    print("Enter the path for the user's image")
    imgPath = input() # Full local path for the image relative to this app.py file

    imgName = imgPath.split('/')[-1]

    # PUT request to add new img object to s3 bucket
    url = f'https://2j02m8iojd.execute-api.us-east-1.amazonaws.com/v1/register/{bucketName}/{subFolder}/{imgName}'
    headers = {'x-amz-meta-Fullname': username,
               'Content-Type': 'binary/octet-stream'
               }


    img = Image.open(imgPath)
    stream = io.BytesIO()
    img.save(stream,format="JPEG")
    imgBin = stream.getvalue()

   
    r = requests.put(url, data=imgBin, headers=headers)
    print(r)

# Verify Function used to verify a new user
def verify():
    print("Verifying user\n")
    print("Enter the path for the user's image")
    imgPath = input() # Full local path for the image relative to this app.py file
    
    img = Image.open(imgPath)
    stream = io.BytesIO()
    img.save(stream,format="JPEG")
    imgBin = stream.getvalue()

    base64_bytes = base64.b64encode(imgBin)
    base64_string = base64_bytes.decode("ascii")

    url = 'https://2j02m8iojd.execute-api.us-east-1.amazonaws.com/v1/verify'

    data = {'stateMachineArn': 'arn:aws:states:us-east-1:005711172119:stateMachine:FaceRecognitionStateMachine',
            'input': '{\"imgData\": \"' + base64_string + '\"}'
            }
    data = json.dumps(data)
    r = requests.post(url, data=data)
    print(r)





# ----- Start of Execution -------------
choice = input("Welcome to my Face Recognition script\nPress (1) to register a new user to db\nPress (2) to verify a user\n")

if(choice == '1'): register()
elif(choice == '2'): verify()
else: print("Your input was: " + choice +"\t Please try again and enter either 1 or 2")