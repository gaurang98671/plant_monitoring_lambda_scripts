import json
import boto3
import math
from datetime import datetime

def lambda_handler(event, context):
   
    # TODO implement
    db_table = boto3.resource('dynamodb').Table('users')
    
    
    #Fetch user email and password
    try:
        data = json.loads(event["body"])
    except:
        return {
        'statusCode': 400,
        'body': "No values provided"
    }
    
    try:
        user_email= data["user_email"]
        user_password = data["user_password"]
      

    except:
         return {
        'statusCode': 400,
        'body': "Missing values"
    }
    
    
    #Check if user exist for respective email and password and return user_id for successful login
    response = db_table.get_item(Key={'email': user_email})
    
    if "Item" in response.keys():

        
        
        user_data= response["Item"]
        if user_data['user_password'] == user_password:
            res= {
                "user_id": str(user_data["user_id"]),
                "user_name": str(user_data["user_name"])
            }
            return{
            'statusCode': 200,
            'body': str(res)}
        else:
            return{
        'statusCode': 400,
        'body': "Incorrect email or password"}
            
        
        
    else:
        return {
        'statusCode': 400,
        'body': "Incorrect email or password!"
    }


    
    
   