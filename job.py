import subprocess
from dht22Service import DHT22CurrentTemp
from time import sleep
subprocess.call("pigpiod")
sleep(30)
current = DHT22CurrentTemp()
current.run()