# PCM60X-MQTT-CODE
Here an simple example request datas from an PCM60X Inverter and post it via MQTT to a broker

source for codes: THANKS to https://github.com/njfaria (help me for understand CRC code and gives me special information about some crc handling)

source for the crc.php pased on this forum:
https://www.szenebox.org/archive/index.php/t-4319.html user NIMBUS

This is an example how you can request datas from an PCM60X Inverter with python 3 code and an 
What you need to do is connect your raspberry pi with the existing RS232 cable, and buy an adapter to USB (pl2303 chip) or use an serielle interface adapter.
```My adapter is an UGREEN USB auf RS232 Seriell Kabel USB Seriell DB9 mit PL2303 Chipsatz (1M) (Search in AMAZON)```

After you have connect your Adapter with your Rasbery Pi and the RS232 Cabel from your Inverter open a shell window and :

1. open the shell window and call: ls -l /dev/serial/by-id
find the adapter 
![alt text](https://raw.githubusercontent.com/solarsnoop/PCM60X-Monitor/master/serport.jpg)
In this example it the: usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0

Please copy your result for the Prolific controler and use it in the same way like this:
ser = serial.Serial(port='/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0',baudrate=2400,timeout=2) 
if you use this sytax and not the ttyUSBx Syntex, you will not have the Problem with USB Port switching , after reboot from the PI. 

ATTENTION ALL CODE HAVE THE FIX SYNTEX LIKE:
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=2400,timeout=2)

please modifiy your Code depending on your port list:
ser = serial.Serial(port='/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0',baudrate=2400,timeout=2) 

This is what you need modify in the code below:
```
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
```
If you call this python3 code in a cron job frequently, your broker get update in the intervall you choosed
you will find the the datas in your broker under solpiplog/PCM60_1
the cronjob or this script should call with python3 flename.py (filename you choosed for this script).


