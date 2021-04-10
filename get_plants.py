import json
import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    # Check weather user exists in user table
    db_table = boto3.resource('dynamodb').Table('users')
   
    #Fetch plant_id and other sensor data
    try:
        user_id = event['queryStringParameters']["user_id"]
    except:
        return {
        'statusCode': 400,
        'body': "No parameters"
    }
    
   
    
    response = db_table.scan(
        FilterExpression=  Attr('user_id').eq(user_id)
        )
        
    
    
    if len(response["Items"]) is not 0:
        plant_table = boto3.resource('dynamodb').Table('plant')
        plants= plant_table.scan(FilterExpression= Attr('user_id').eq(user_id))
        
        res={
            "plants": plants["Items"]
            
        }
        
        return{
        'statusCode': 200,
        'body': str(res)}
    else:
       
        return {
        'statusCode': 400,
        'body': "User not found"
    }

