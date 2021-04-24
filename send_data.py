import csv
import requests
import time

pot_id = input("Enter pot id")
while True:
    #TODO
    #Open csv file DONE
    #Fetch last row DONE
    #Post row data DONE
    #Print response DONE
    #Sleep for 10 seconds DONE
    with open('plant_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        l = list(csv_reader)

        humidity = int(float(l[-1][0]))
        temperature = int(float(l[-1][1]))
        light = int(float(l[-1][2]))
        moisture = "Yes"
        req = {"temperature": str(temperature), "pot_id": str(pot_id), "humidity": str(humidity),
               "light": str(light), "moisture": str(moisture)}
        print(req)

        r = requests.post("https://zlnhbt4ogh.execute-api.us-east-1.amazonaws.com/send_sensor_data", json=req)

        print(r.content)
        csv_file.close()
        time.sleep(10)

