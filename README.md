# DHT22 Service

A service to read a DHT22 sensor that is connected to a raspberry pi. The service will read the temperature and humidity every 5 seconds and update a mongodb with the current temperature and humidity. On each hour the service will also update the mongodb with the hourly temperature and humidity.

By default the service reads from gpio 12 and reads every 5 seconds (the DHT22 sensor won't work well if faster then 3 seconds). If you want to change the values then simply edit the main method (I'll be pulling these values out to be arguments that you can pass from the commandline in on the next update).


## Prerequisites
You need to have the following installed:

- [MongoDB](http://www.mongodb.org) set this up as a service to run when the pi first boots up
- [pymongo](https://docs.mongodb.com/getting-started/python/client/)
- [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)
- [pigpio as a service](https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=103752)
- [DHT22 Sensor](https://www.adafruit.com/product/385) and everything else (breadboard, wires, ribbon cable to connect breadboard to the pi) to connect this to your raspberry pi

## Install

Install and run via Docker ([DHT22 Service Docker Repository](https://hub.docker.com/r/cpitzak/weather-dht22-service/)):
```
$ docker pull cpitzak/weather-dht22-service:1.0.0
$ docker run -e "DHT22_SERVICE_MONGO_URL=mongodb://your_monog_url/weatherdb" \
             -e "DHT22_SERVICE_DELAY=5" \
             -e "DHT22_SERVICE_GPIO=12" \
             --cap-add SYS_RAWIO \
             --device /dev/mem \
             --device /dev/vcio \
             -p 8888:8888 \
             cpitzak/weather-dht22-service
```

Or Build a docker image and run
```
$ docker build -t cpitzak/weather-dht22-service .
$ docker run -e "DHT22_SERVICE_MONGO_URL=mongodb://your_monog_url/weatherdb" \
             -e "DHT22_SERVICE_DELAY=5" \
             -e "DHT22_SERVICE_GPIO=12" \
             --cap-add SYS_RAWIO \
             --device /dev/mem \
             --device /dev/vcio \
             -p 8888:8888 \
             cpitzak/weather-dht22-service
```

Or to setup Manually
```
$ sudo mkdir /apps
$ sudo chown pi /apps
$ cd /apps
$ git clone https://github.com/cpitzak/dht22Service.git
$ cd dht22Service
$ sudo cp init.d/dht22Service /etc/init.d/
$ sudo chmod 755 /etc/init.d/dht22Service
$ sudo update-rc.d dht22Service defaults
$ sudo update-rc.d dht22Service enable
$ sudo systemctl daemon-reload
$ sudo service dht22Service start
```

This service is a dependency to my other project [weatherWeb](https://github.com/cpitzak/weatherWeb).

