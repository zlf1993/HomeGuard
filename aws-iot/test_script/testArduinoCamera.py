import paho.mqtt.client as mqtt
import json
import sys
import threading
import time
import serial
import cv2
from camera import Camera
from ArduinoSerial import ArduinoSerial
from image2googledrive import Image2GoogleDrive

cafile = "/home/pi/Documents/aws-iot/root-CA.crt"
cerfile = "/home/pi/Documents/aws-iot/62c12da123-certificate.pem.crt"
keyfile = "/home/pi/Documents/aws-iot/62c12da123-private.pem.key"

SERVER = "a37i47xeh8qin6-ats.iot.ca-central-1.amazonaws.com"
PORT = 8883

TOPIC = "iot/topic"
QOS = 1

message = {"default":"https://drive.google.com/drive/folders/12ilLCJvXGdoMvSJ6pWSf7PLjaDSnKizI?usp=sharing"}
Data_Out = json.dumps(message)

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))
    
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    
cam = Camera(384, 192, False)
arser = ArduinoSerial()

readTh = threading.Thread(target = arser.readSerial)
threads = [readTh]
for t in threads:
    t.setDaemon(True)
    t.start()

while True:
    while arser.cameraState =="1":
        img = cam.takePicture()
        cv2.imshow("Image", img)
        cv2.waitKey(30)
    cv2.destroyAllWindows()




