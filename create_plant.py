import json
import boto3
from uuid import uuid4

def lambda_handler(event, context):
    plant_table = boto3.resource('dynamodb').Table('plant')
    plant_data_table= boto3.resource("dynamodb").Table('plant_data')
    # TODO implement
    #pot_id, plant_name, botanical_name, user_id, last_updated=Null
    
    #Fetch values from request body
    try:
        
        data = json.loads(event["body"])
    except:
        return {
        'statusCode': 200,
        'body': "No values provided"
    }
    
    
    try:
        user_id= data["user_id"]
        plant_name= data["plant_name"]
        botanical_name= data["botanical_name"]
        pot_id= data["pot_id"]
        nick_name= data["nick_name"]

    except:
         return {
        'statusCode': 200,
        'body': "Missing values"
    }
    #Check weather pot id is already in use or not
    response = plant_table.get_item(Key={'pot_id': pot_id})
    if "Item" in response.keys():
        return{
        'statusCode': 200,
        'body': "Pot is being used"}
        
    else:
        #Fetch ideal values from plant data 
        response= plant_data_table.get_item(Key={"botanical_name": botanical_name})
        if "Item" not in response.keys():
            
            return {
            'statusCode': 200,
            'body': "No such plant found in database"}
        
        else:
            plant_data= response["Item"]
            ideal_data=[]
            ideal_data.append(plant_data["temperature_range"])
            ideal_data.append(plant_data["light_range"])
            ideal_data.append(plant_data["humidity_range"])
            
            #Add to plants table
            plant_table.put_item(
                Item={
                    "pot_id": pot_id,
                    "user_id": user_id,
                    "ideal_data": dict(
                        {
                            "temperature_range": ideal_data[0],
                            "light_range": ideal_data[1],
                            "humidity_range": ideal_data[2]
                        }
                        ),
                        
                    "nick_name": nick_name,
                    "plant_name": plant_name,
                    "botanical_name": botanical_name,
                    "last_updated": "0",
                    "data": [],
                    "suggesstions": []
                }
                )
            
            return{
            'statusCode': 200,
            'body': "Data added"}
    

    
    
   
    
  
   
    
   
    
   
   