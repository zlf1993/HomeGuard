import paho.mqtt.client as mqtt
import json
import sys
from camera import Camera
import threading
import cv2
import time
from ArduinoSerial import ArduinoSerial
from image2googledrive import Image2GoogleDrive

TOPIC = "iot/topic"
motion = {
    "state": {
        "desired":{
            "motion":"2",
        }
    }
}
pedestrian = {
    "state": {
        "desired":{
            "pedestrian":"0",
        }
    }
}
#print(Data_Out)
cafile = "/home/pi/Documents/aws-iot/root-CA.crt"
cerfile = "/home/pi/Documents/aws-iot/62c12da123-certificate.pem.crt"
keyfile = "/home/pi/Documents/aws-iot/62c12da123-private.pem.key"
SERVER = "a37i47xeh8qin6-ats.iot.ca-central-1.amazonaws.com"
PORT = 8883
subscribe_list = [("topic/img", 0), ("$aws/things/BlackPi/shadow/update/accepted", 1)]

# set camera
cam = Camera(320, 240,160,120, json=True)
# set Arduino
arser = ArduinoSerial()
# set google_drive
imgupload = Image2GoogleDrive()
# set read thread
readTh = threading.Thread(target = arser.readSerial)
readTh.setDaemon(True)
readTh.start()

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))

def on_message(client, userdata, msg):
    # print(msg.topic)
    if msg.topic == "$aws/things/BlackPi/shadow/update/accepted":
        shadow = json.loads(msg.payload)
        
        if 'system' in shadow['metadata']['desired'].keys():
            system_timestamp = shadow['metadata']['desired']['system']['timestamp']
            if system_timestamp > client.system_time:
                system = int(shadow['state']['desired']['system'].strip('\n').strip('\r'))
                client.system_state = system
                client.system_time = system_timestamp        
            
        if 'angle' in shadow['metadata']['desired'].keys():
            angle_timestamp = shadow['metadata']['desired']['angle']['timestamp']
            if angle_timestamp > client.ang_time:
                client.ang_time = angle_timestamp
                angle = shadow['state']['desired']['angle'].strip('\n').strip('\r')
                client.aser.writeSerial(bytes(angle, encoding="gbk"))
                   
        if 'camera' in shadow['metadata']['desired'].keys(): 
            camera_timestamp = shadow['metadata']['desired']['camera']['timestamp']
            if camera_timestamp > client.camera_time:
                camera = int(shadow['state']['desired']['camera'].strip('\n').strip('\r'))
                client.camera_state = camera
                client.camera_time = camera_timestamp
                
        if 'face' in shadow['metadata']['desired'].keys():    
            face_timestamp = shadow['metadata']['desired']['face']['timestamp']
            # tiemstap type int
            if face_timestamp > client.face_time:
                face = int(shadow['state']['desired']['face'].strip('\n').strip('\r'))
                client.face_state = face
                client.face_time = face_timestamp      
        
    if msg.topic == "topic/img":
        shadow = json.loads(msg.payload)
        img_json = shadow['state']['desired']['img']
        war_dic = json.loads(dicJson)
        bytes2 = war_dic["state"]["desired"]["img"]
               #print(bytes2)
        b1 = bytes(bytes2, encoding="gbk")
        b2 = codecs.escape_decode(b1, 'hex-escape')[0]
        nparr_img = cPickle.loads(b2)
        cv2.imshow("Image", nparr_img)
        key = cv2.waitKey(5)


# set mqtt
# arn:aws:iot:ca-central-1:369639037617:thing/BlackPi
client = mqtt.Client(client_id="", clean_session=True, userdata=None, transport="tcp")
client.tls_set(cafile, cerfile, keyfile)
client.on_connect = on_connect
client.on_message = on_message
pro_pedestrian = "10"
client.ang_time = 0
client.aser = arser
client.system_time = 0
client.system_state = 1
client.camera_time = 0
client.camera_state = 0
client.face_time = 0
client.face_state = 0
client.motion_time = 0
client.motion_state = 0


client.connect(host=SERVER, port=PORT, keepalive=60, bind_address="")
client.loop_start()
client.subscribe(subscribe_list)
upload_state = 0
motion_state = "2" # no motion
while True:
    # sernsor data upload
    if arser.motion == "3" and "3" != motion_state:
        motion['state']['desired']['motion'] = "True"
        motion_state = "3"
        Data_Out = json.dumps(motion)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
    if arser.motion == "2" and "2" != motion_state:
        motion['state']['desired']['motion'] = "Flase"
        motion_state = "2"
        Data_Out = json.dumps(motion)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
        
    if arser.pedestrian != pro_pedestrian:
        pro_pedestrian = arser.pedestrian
        pedestrian['state']['desired']['pedestrian'] = pro_pedestrian
        datajson = json.dumps(pedestrian)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=datajson, qos=1, retain=False)
    # camera system condition
    if client.system_state == 1:
        if client.face_state == 0:
            upload_state = 0
            if arser.cameraState == "1" or client.camera_state == 1:     
                imgjson = cam.takePicture()
                # print(imgjson)
                # client.publish(topic="topic/img", payload=imgjson, qos=0, retain=False)
                client.publish(topic="topic/img", payload=imgjson, qos=0, retain=False)
                time.sleep(0.04)
                if client.face_state == 1:
            else:
                # upload_state = 0
                cam.releaseCam()
                cam = Camera(320, 240,160,120, json=True)
        elif  arser.cameraState == "1" and client.face_state == 1:
            if upload_state == 0:
                
                upload_state = 1
                # readTh = threading.Thread(target = arser.readSerial)
                # readTh.setDaemon(True)
                # readTh.start()
            else:
                imgjson = cam.takePicture()
                client.publish(topic="topic/img", payload=imgjson, qos=0, retain=False)
        else:
            upload_state = 0
            cam.releaseCam()
            cam = Camera(320, 240,160,120, json=True)
            
cam.releaseCam()   
client.loop_stop()
client.disconnect()  





