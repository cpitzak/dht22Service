import datetime
import DHT22
import pigpio
from time import sleep
from pymongo import MongoClient


class DHT22CurrentTemp:


    def __init__(self, delay, gpio):
        self.delay = delay
        pi = pigpio.pi()
        self.dht22 = DHT22.sensor(pi, gpio)
        client = MongoClient('localhost', 27017)
        self.db = client.weatherdb
        self.collection_current_room_weather = self.db.current_room_weather
        self.collection_room_weather = self.db.room_weather

    def update_current_room_weather(self, humidity, temp):
        self.collection_current_room_weather.update({'name': 'current_weather'},
                               {"$set": {"temp": temp,
                                         "humidity": humidity}},
                               upsert=True)

    def update_room_weather(self, humidity, temp, now):
        key = "{year}_{month}_{day}_{hour}".format(year=now.year, month=now.month, day=now.day, hour=now.hour)
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

        written = False
        while True:
            humidity, temp = self.read_dht22()
            print "current temp {0} F and humidity {1}%".format(temp, humidity)
            self.update_current_room_weather(humidity, temp)
            now = datetime.datetime.now()
            if now.minute < 2 and written is False:
                print "wrote hourly temp of {0} and humidity {1}%".format(temp, humidity)
                self.update_room_weather(humidity, temp, now)
                written = True
            elif now.minute >= 2:
                written = False
            sleep(self.delay)

if __name__ == "__main__":
    current = DHT22CurrentTemp(5, 12)
    current.run()

