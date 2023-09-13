import time
import serial
import paho.mqtt.publish as publish
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

QPIGS = b"\x51\x50\x49\x47\x53\xB7\xA9\x0D"

MQTT_SERVER = "127.0.0.1" #(Your IP from your broker, if the broker runs on the same device you can use 127.0.0.1)
MQTT_PORT = 1884 #(please modify your Broker port)
MQTT_PATH1 = "solpiplog/PCM60_1/watt"
MQTT_PATH2 = "solpiplog/PCM60_1/strom"
MQTT_PATH3 = "solpiplog/PCM60_1/voltpv"
MQTT_PATH4 = "solpiplog/PCM60_1/temp"
MQTT_PATH5 = "solpiplog/PCM60_1/voltb"
#the adapter name below should used from the result from your  ls -l /dev/serial/by-id request 
ser = serial.Serial(port='/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_BOCMf103Y23-if00-port0', baudrate=2400, timeout=2) 

if ser.isOpen():
    ser.write(QPIGS)
    result = ser.read(68)
    print(result)  
publish.single(MQTT_PATH1, result[31:35].decode('utf-8'), hostname=MQTT_SERVER, port=MQTT_PORT)
publish.single(MQTT_PATH2, result[14:19].decode('utf-8'), hostname=MQTT_SERVER, port=MQTT_PORT)
publish.single(MQTT_PATH3, result[1:6].decode('utf-8'), hostname=MQTT_SERVER, port=MQTT_PORT)
publish.single(MQTT_PATH4, result[38:40].decode('utf-8'), hostname=MQTT_SERVER, port=MQTT_PORT)
publish.single(MQTT_PATH5, result[7:12].decode('utf-8'), hostname=MQTT_SERVER, port=MQTT_PORT)

ser.close()
