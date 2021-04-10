import json
import boto3
from uuid import uuid4

def lambda_handler(event, context):
    
    plant_data_table= boto3.resource("dynamodb").Table('plant_data')
    # TODO implement
    
    
    #Fetch values from request body
    try:
        
        data = json.loads(event["body"])
    except:
        return {
        'statusCode': 400,
        'body': "No values provided"
    }
    
    
    try:
       
        plant_name= data["plant_name"]
        botanical_name= data["botanical_name"]
        humidity_range= data["humidity_range"]
        temperature_range = data["temperature_range"]
        light_range = data["light_range"]
        plant_type= data["plant_type"]

    except:
         return {
        'statusCode': 200,
        'body': "Missing values"
    }
    #Check weather plant with botanical name alredy exists or not
    response =  plant_data_table.get_item(Key={"botanical_name": botanical_name})
    if "Item" in response.keys():
        
        return{
        'statusCode': 400,
        'body': "Plant already exists"}
        
    else:
        plant_data_table.put_item(
            Item={
                "botanical_name": str(botanical_name),
                "plant_name": str(plant_name),
                "plant_type": str(plant_type),
                "temperature_range": str(temperature_range),
                "humidity_range": str(humidity_range),
                "light_range": str(light_range)
            }
            )
            
        return{
            'statusCode': 200,
            'body': "Data added"}
    

    
    
   
    
  