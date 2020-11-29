import socket 
import time
# for raspberry gpio
import RPi.GPIO as gpio
import wiringpi

client_socket = None

def shot(pin):
    global shooted
    if shooted == 0:
        shooted = 1
        message="1"
        client_socket.send(message.encode()) 

HOST = '192.168.0.21'
PORT = 7888
PIN = 2

wiringpi.wiringPiSetup()

# set gpio
gpio.setmode(gpio.BCM)
gpio.setup(PIN, gpio.IN)

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 

print("connect")

gpio.add_event_detect(PIN, gpio.RISING, callback=shot)

while True:
    shooted = 0
    wiringpi.delay(5)
    
client_socket.close() 
gpio.cleanup()
