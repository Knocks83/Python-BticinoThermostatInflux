from time import sleep
import bticino
from influxdb import InfluxDBClient
from datetime import datetime, timezone

from dotenv import load_dotenv
from os import getenv
from os.path import dirname, realpath

import logging

load_dotenv(dotenv_path=dirname(realpath(__file__))+'/config.env')
logging.basicConfig(encoding='utf-8', level=logging.INFO)

if getenv('CalculateAbsolutePath') == 'true':
    refreshTokenPath = dirname(realpath(__file__))+'/'+getenv('RefreshFileName')
else:
    refreshTokenPath = getenv('RefreshFileName')

# Generate the objects
bticinoObj = bticino.Bticino(getenv('ClientID'), getenv('ClientSecret'), getenv('Redirect'), getenv('SubscriptionKey'), getenv('PlantID'), getenv('ModuleID'), getenv('AuthEndpoint'), getenv('APIEndpoint'), refreshTokenPath)
client = InfluxDBClient(host=getenv('InfluxHost'), port=getenv('InfluxPort'), database=getenv('InfluxDatabase'))

while True:
    logging.debug("Starting loop")
    bticinoObj.login()
    logging.debug('Logged in!')
    measures = bticinoObj.measures()
    logging.debug("Measurements: " + str(measures))

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
        'time': datetime.now(timezone.utc).isoformat()
    }]
    logging.debug("Point: " + str(point))
    client.write_points(point)

    logging.debug("Finished loop, starting sleep")
    sleep(int(getenv('RequestDelay')))
