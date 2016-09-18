import datetime
import os
import pigpio
from ConfigParser import SafeConfigParser
from lib import DHT22
from pymongo import MongoClient
from time import sleep


class DHT22CurrentTemp:


    def __init__(self):
        parser = SafeConfigParser()
        cwd = os.path.dirname(os.path.realpath(__file__))
        parser.read(os.path.join(cwd, 'config.ini'))
        self.delay = int(os.getenv('DHT22_SERVICE_DELAY', parser.get('general', 'delay')))
        gpio = int(os.getenv('DHT22_SERVICE_GPIO', parser.get('general', 'gpio')))
        pi = pigpio.pi()
        self.dht22 = DHT22.sensor(pi, gpio)
        mongodb_url = os.getenv('DHT22_SERVICE_MONGO_URL', parser.get('urls', 'mongodb'))
        client = MongoClient(mongodb_url)
        self.db = client.weatherdb
        self.collection_current_room_weather = self.db.current_room_weather
        self.collection_room_weather = self.db.room_weather

    def update_current_room_weather(self, humidity, temp):
        self.collection_current_room_weather.update({'name': 'current_weather'},
                               {"$set": {"temp": temp,
                                         "humidity": humidity}},
                               upsert=True)
    def get_room_weather_db_key(self, now):
        key = "{year}_{month}_{day}_{hour}".format(year=now.year, month=now.month, day=now.day, hour=now.hour)
        return key

    def update_room_weather(self, humidity, temp, now):
        key = self.get_room_weather_db_key(now)
        self.collection_room_weather.update({'date_hour': key},
                                        {"$set": {"temp": temp,
                                                  "humidity": humidity,
                                                  "hour": now.hour,
                                                  "month": now.month,
                                                  "day": now.day,
                                                  "year": now.year}},
                                       upsert=True)

    def celcius_to_fahrenheit(self, celcius):
        return celcius * (9/5.0) + 32

    def read_dht22(self):
        self.dht22.trigger()
        humidity = '{0:.2f}'.format(round(self.dht22.humidity(), 2))
        temp = '{0:.2f}'.format(self.celcius_to_fahrenheit(round(self.dht22.temperature(), 2)))
        return humidity, temp

    def run(self):
        # clear out initial -99999 readings
        self.read_dht22()
        sleep(3)
        self.read_dht22()
        sleep(3)

        room_hour_writes = {}
        needs_reset = False
        now = datetime.datetime.now()
        key = self.get_room_weather_db_key(now)
        # prevent updating hourly if already exists in database
        db_writes_enabled = True if self.collection_room_weather.find_one({"date_hour": key}) == None else False
        while True:
            humidity, temp = self.read_dht22()
            print "current temp {0} F and humidity {1}%".format(temp, humidity)
            self.update_current_room_weather(humidity, temp)
            now = datetime.datetime.now()
            if db_writes_enabled:
                if needs_reset and now.hour == 0:
                    room_hour_writes = {}
                    needs_reset = False
                if now.hour not in room_hour_writes:
                    room_hour_writes[now.hour] = True
                    print "updated database with current temp {0} F and humidity {1}%".format(temp, humidity)
                    self.update_room_weather(humidity, temp, now)
                    if now.hour == 23:
                        needs_reset = True
            else:
                room_hour_writes[now.hour] = True
                db_writes_enabled = True
            sleep(self.delay)

if __name__ == "__main__":
    current = DHT22CurrentTemp()
    current.run()