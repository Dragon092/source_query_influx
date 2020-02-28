import a2s
from datetime import datetime
from influxdb import InfluxDBClient
import json

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except IOError:
    print("Error opening config file")
    exit(1)

points = []

for name, gameserver in config["gameservers"].items():
    address = (gameserver["ip"], gameserver["port"])

    info = a2s.info(address)

    print(info)
    #print(a2s.players(address))
    #print(a2s.rules(address))

    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    point = {
        "measurement": name + '_player_count',
        "time": current_time,
        "fields": {
            "value": info.player_count
        }
    }
    points.append(point)


# Insert into InfluxDB
client = InfluxDBClient(config["influx"]["host"], config["influx"]["port"], config["influx"]["user"], config["influx"]["password"], config["influx"]["database"])
client.write_points(points)
