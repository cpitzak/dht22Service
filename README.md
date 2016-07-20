# DHT22 Service

A service to read a DHT22 sensor that is connected to a raspberry pi. The service will read the temperature and humidity every 5 seconds and update a mongodb with the current temperature and humidity. On each hour the service will also update the mongodb with the hourly temperature and humidity.

By default the service reads from gpio 12 and reads every 5 seconds (the DHT22 sensor won't work well if faster then 3 seconds). If you want to change the values then simply edit the main method (I'll be pulling these values out to be arguments that you can pass from the commandline in on the next update).


## Prerequisites
You need to have the following installed:

- [MongoDB](http://www.mongodb.org) set this up as a service to run when the pi first boots up
- [pymongo](https://docs.mongodb.com/getting-started/python/client/)
- [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)
- [pigpio as a service](https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=103752)
- [DHT22 Sensor](https://www.adafruit.com/product/385) and everything else (breadboard, wires, Ribbon cable to connect breadboard to the pi) to connect this to your raspberry pi

## Install

Note: make sure mongdb is running whenever using this service


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

