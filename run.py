import bticino
from influxdb_client import InfluxDBClient, Point
from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from os.path import dirname, realpath

load_dotenv(dotenv_path=dirname(realpath(__file__))+'/config.env.bak')

if getenv('CalculateAbsolutePath') == True:
    refreshTokenPath = dirname(realpath(__file__))+'/'+getenv('RefreshFileName')
else:
    refreshTokenPath = getenv('RefreshFileName')

# Generate the objects
bticinoObj = bticino.Bticino(getenv('ClientID'), getenv('ClientSecret'), getenv('Redirect'), getenv('SubscriptionKey'), getenv('PlantID'), getenv('ModuleID'), getenv('AuthEndpoint'), getenv('APIEndpoint'), refreshTokenPath)

influxClient = InfluxDBClient(url=getenv('InfluxHost'), token=getenv('InfluxToken'), org=getenv('InfluxOrg'))
influxWriteAPI = influxClient.write_api()



while True:
    bticinoObj.login()
    measures = bticinoObj.measures()

    point = ( 
        Point(getenv('InfluxMeasurementName'))
        .tag('sensorType', 'BticinoThermostat')
        .tag('sensorID', getenv('ModuleID'))
        .field('temperature', measures['temperature'])
        .field('humidity', measures['humidity'])
        .field('status', measures['status'])
        .time(datetime.now().isoformat())
    )

    influxWriteAPI.write(bucket=getenv('InfluxBucket'), org=getenv('InfluxOrg'), record=point)
    influxWriteAPI.flush()
