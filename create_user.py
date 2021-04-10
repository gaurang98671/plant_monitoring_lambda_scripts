import json
import boto3
from uuid import uuid4

def lambda_handler(event, context):
    
    # TODO implement
    db_table = boto3.resource('dynamodb').Table('users')
   
    #Fetch plant_id and other sensor data
    try:
        data = json.loads(event["body"])
    except:
        return {
        'statusCode': 200,
        'body': "No values provided"
    }
    
    try:
        user_name= data["user_name"]
        user_email = data["user_email"]
        user_password = data["user_password"]

    except:
         return {
        'statusCode': 200,
        'body': "Missing values"
    }
    
    response = db_table.get_item(Key={'email': user_email})
    
    if "Item" in response.keys():
        return{
        'statusCode': 200,
        'body': "User alredy exists"}
    else:
        db_table.put_item(
            Item= {
                'user_id':  str(uuid4()),
                'email' : user_email,
                'user_name': user_name,
                'user_password': user_password
                }
            )
        return {
        'statusCode': 200,
        'body': "User created"
    }


    
    
   