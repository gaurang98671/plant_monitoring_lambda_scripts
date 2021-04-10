import json
import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    plant_table = boto3.resource('dynamodb').Table('plant')
    user_table  = boto3.resource('dynamodb').Table('users')
   
  
    #Fetch values from request body
    try:
         data = json.loads(event["body"])
    except:
        return {
        'statusCode': 400,
        'body': "No values provided"
    }
    
    
    try:
        
        user_id= data["user_id"]
        pot_id= data["pot_id"]
        
    except:
         return {
        'statusCode': 400,
        'body': "Missing values"
    }
    
    #Check weather user_exists in user table
    response = user_table.scan(
        FilterExpression=  Attr('user_id').eq(user_id)
        )
    
    if len(response["Items"]) is 0:
        return{
            'statusCode': 400,
            'body': "User not found"}
        
    #Check weather plant with pot_id exists in plant table
    response = plant_table.get_item(Key={'pot_id': pot_id})
    if "Item" in response.keys():
        
        #delete item and return deleted item
        plant_table.delete_item(
            Key={'pot_id': pot_id}
            )
        return{
        'statusCode': 200,
        'body': str(response["Item"])}
        
    else:
        
        return{
            'statusCode': 400,
            'body': "Not pot found"}
    
        
            
           

    
    
   
    
  
   
    
   
    