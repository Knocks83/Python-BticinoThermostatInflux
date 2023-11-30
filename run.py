from time import sleep
import bticino
import influxdb_client
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
influx_client = influxdb_client.InfluxDBClient(url=getenv('InfluxURL'), token=getenv('InfluxToken'), org=getenv('InfluxOrg'))
write_api = influx_client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS)

while True:
    logging.debug("Starting loop")
    try:
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
        write_api.write(bucket=getenv('InfluxBucket'), org=getenv('InfluxOrg'), record=point)
    except KeyError as e:
        logging.error('KeyError while executing loop! ' + str(e))
    except Exception as e:
        logging.error('Generic exception while executing loop! ' + str(e))
    finally:
        logging.debug("Finished loop, starting sleep")
        sleep(int(getenv('RequestDelay')))
