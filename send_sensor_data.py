import json
import boto3
import math
from datetime import datetime
from botocore.exceptions import ClientError
def lambda_handler(event, context):
    allowed_range_high=5
    allowed_range_low=5
    # TODO implement
    db_table = boto3.resource('dynamodb').Table('plant')
    last_updated=datetime.now()
    
    #Fetch plant_id and other sensor data
    try:
        data = json.loads(event["body"])
    except:
        return {
        'statusCode': 400,
        'body': "No values provided"
    }
    
    try:
        plant_id= data["pot_id"]
        plant_temperature = int(data["temperature"])
        plant_light = int(data["light"])
        plant_humidity= int(data["humidity"])
        plant_moisture= data["moisture"]

    except:
         return {
        'statusCode': 400,
        'body': "Missing values"
    }
    
    response = db_table.get_item(Key={'pot_id': plant_id})
    
    if "Item" in response.keys():

        #Compare values add suggesstions
        
        
        ideal_plant_data= response["Item"]["ideal_data"]
        suggesstions=[] 
        
        #Check for temperature
        temp_range = ideal_plant_data["temperature_range"].split("-")
        temp_low= int(temp_range[0])
        temp_high= int(temp_range[1])
        if(plant_temperature<temp_low): 
            suggesstions.append("Low temperature")
        elif plant_temperature> temp_high:
            suggesstions.append("High temperature")
        else:
            suggesstions.append("Perfect temperature")
       
            
        #Check for humidity
        humidity_range = ideal_plant_data["humidity_range"].split("-")
        humidity_low= int(temp_range[0])
        humidity_high= int(temp_range[1])
        if(plant_humidity<humidity_low): 
            suggesstions.append("Low humidity")
        elif plant_humidity> humidity_high:
            suggesstions.append("High humidity")
        else:
            suggesstions.append("Perfect humidity")
            
        #Check for light
        light_range = ideal_plant_data["light_range"].split("-")
        light_low= int(light_range[0])
        light_high= int(light_range[1])
        if(plant_light<light_low): 
            suggesstions.append("Low light")
        elif plant_light> light_high:
            suggesstions.append("High light")
        else:
            suggesstions.append("Perfect light")
            
        #Check for mousture    
        if(plant_moisture=="No"):
            suggesstions.append("Watering needed!")
            
        #Add plant data along with time stamp to plant table
        try:
            
            db_table.update_item(
            Key={'pot_id': plant_id},
           
            UpdateExpression='SET #name.temperature= :temp, #name.humidity = :humidity, #name.light= :light, #name.moisture= :moisture, #last_updated= :timestamp1, #suggesstions= :sugg',
            ExpressionAttributeValues={
            ":temp": int(plant_temperature),
            ":humidity": int(plant_humidity),
            ":light" : int(plant_light),
            ":moisture" : str(plant_moisture),
            ":timestamp1" : str(last_updated.isoformat()),
            ":sugg": suggesstions,
            },
            ExpressionAttributeNames={
            "#name": "data",
            "#last_updated": "last_updated",
            "#suggesstions" : "suggesstions"
            })
               
        
     
        except ClientError as e:
            
                
            if e.response['Error']['Code'] == 'ValidationException':
                
            # Creating new top level attribute `info` (with nested props) 
            # if the previous query failed
                response = db_table.update_item(
                    Key={"pot_id": plant_id},
                    UpdateExpression="set #attrName = :attrValue, #last_updated= :timestamp1, #suggesstions= :sugg",
                    ExpressionAttributeNames = {"#attrName" : "data", "#last_updated": "last_updated", "#suggesstions": "suggesstions"},
                    ExpressionAttributeValues={':attrValue': {'temperature': int(plant_temperature), 'humidity': int(plant_humidity), 'light': int(plant_light), 'moisture': str(plant_moisture)},
                    ":timestamp1":str(last_updated.isoformat()),
                    ":sugg": suggesstions
                        
                    }
                    )
                   
        return{
        'statusCode': 200,
        'body': "Plant data updated"}
    else:
        return {
        'statusCode': 400,
        'body': "Plant is not registered"
    }


    
    
   