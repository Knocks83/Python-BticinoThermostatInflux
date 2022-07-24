from time import sleep
import bticino
from influxdb import InfluxDBClient
from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from os.path import dirname, realpath

load_dotenv(dotenv_path=dirname(realpath(__file__))+'/config.env')

if getenv('CalculateAbsolutePath') == True:
    refreshTokenPath = dirname(realpath(__file__))+'/'+getenv('RefreshFileName')
else:
    refreshTokenPath = getenv('RefreshFileName')

# Generate the objects
bticinoObj = bticino.Bticino(getenv('ClientID'), getenv('ClientSecret'), getenv('Redirect'), getenv('SubscriptionKey'), getenv('PlantID'), getenv('ModuleID'), getenv('AuthEndpoint'), getenv('APIEndpoint'), refreshTokenPath)
client = InfluxDBClient(host=getenv('InfluxHost'), port=getenv('InfluxPort'), database=getenv('InfluxDatabase'))

while True:
    bticinoObj.login()
    measures = bticinoObj.measures()

    point = [{
        'measurement': getenv('InfluxMeasurementName'),
        'tags': {
            'sensorType': 'BticinoThermostat',
            'sensorID': getenv('ModuleID')
        },
        'fields': {
            'temperature': float(measures['temperature']),
            'humidity': float(measures['humidity']),
            'status': measures['status']
        },
        'time': datetime.now().isoformat()
    }]
    client.write_points(point)

    sleep(int(getenv('RequestDelay')))
