import paho.mqtt.client as mqtt
import json
import sys
from camera import Camera
import threading
import cv2
import time
import _pickle as cPickle
from ArduinoSerial import ArduinoSerial
from image2googledrive import Image2GoogleDrive
import os
TOPIC = "iot/topic"
motion = {
    "state": {
        "desired":{
            "motion":"2",
        }
    }
}

temp = {
    "state": {
        "desired":{
            "temperature":"0",
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
dic = {
    "state": {
        "desired":{
            "face": None
        }
    }
}
#print(Data_Out)
cafile = "/home/pi/Documents/aws-iot/root-CA.crt"
cerfile = "/home/pi/Documents/aws-iot/62c12da123-certificate.pem.crt"
keyfile = "/home/pi/Documents/aws-iot/62c12da123-private.pem.key"
SERVER = "a37i47xeh8qin6-ats.iot.ca-central-1.amazonaws.com"
PORT = 8883
subscribe_list = [("$aws/things/BlackPi/shadow/update/accepted", 1),("topic/face",1)]

# set camera
cam = Camera(320, 240,160,120, json=True)
# set Arduino
arser = ArduinoSerial()
# set google_drive
# imgupload = Image2GoogleDrive()
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
have_face = 0
pede_sta = "5"
temp_state = "0"
imgpath = "/home/pi/Documents/aws-iot/Image/CameraFrame.jpeg"
while True:
    # sernsor data upload
    if arser.motion == "3" and "3" != motion_state:
        print("motion actived")
        motion['state']['desired']['motion'] = "True"
        motion_state = "3"
        Data_Out = json.dumps(motion)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
    if arser.motion == "2" and "2" != motion_state:
        print("motion actived")
        motion['state']['desired']['motion'] = "Flase"
        motion_state = "2"
        Data_Out = json.dumps(motion)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
        
    if arser.temperature == "4" and "4" != temp_state:
        print("temp high")
        temp['state']['desired']['temperature'] = "High"
        temp_state = "4"
        Data_Out = json.dumps(temp)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
    if arser.temperature == "5" and "5" != temp_state:
        print("temp low")
        temp['state']['desired']['temperature'] = "Low"
        temp_state = "5"
        Data_Out = json.dumps(temp)
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)
        
    if arser.pedestrian == "6" and "6" != pede_sta:
        pede_sta = "6"
        pedestrian['state']['desired']['pedestrian'] = pede_sta
        datajson = json.dumps(pedestrian)
        print("send pedestrian")
        client.publish(topic="$aws/things/BlackPi/shadow/update", payload=datajson, qos=1, retain=False)
    if arser.pedestrian == "7" and "7" != pede_sta:
        #print("person go away")
        pede_sta = "7"
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
            else:
                cam.releaseCam()
                cam = Camera(320, 240,160,120, json=True)
        elif  arser.cameraState == "1" and client.face_state == 1:
            if upload_state == 0:
                print("try to find face")
                cam.savePicture()
                if os.path.exists(imgpath):
                    frame = cv2.imread(imgpath)
                    net = cv2.dnn.readNet('face-detection-adas-0001.xml','face-detection-adas-0001.bin')
                    net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
                    blob = cv2.dnn.blobFromImage(frame, size=(672, 384), ddepth=cv2.CV_8U)
                    net.setInput(blob)
                    out = net.forward()
                    for detection in out.reshape(-1, 7):
                        confidence = float(detection[2])
                        xmin = int(detection[3] * frame.shape[1])
                        ymin = int(detection[4] * frame.shape[0])
                        xmax = int(detection[5] * frame.shape[1])
                        ymax = int(detection[6] * frame.shape[0])
                        if confidence > 0.5:
                            haveface = 1
                            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
                    if haveface == 1:
                        print("find face!")
                        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        frame_resize = cv2.resize(frame_gray, (160, 120), interpolation=cv2.INTER_CUBIC)
                        bytesImg = cPickle.dumps(frame_resize)
                        strImg = s = str(bytesImg)[2:-1]
                        dic["state"]["desired"]["face"] = strImg
                        dicJson = json.dumps(dic)
                        client.publish(topic="topic/face", payload=dicJson, qos=1, retain=False)
                        print("send face")
                        havaface = 0
                        upload_state = 1
                # readTh = threading.Thread(target = arser.readSerial)
                # readTh.setDaemon(True)
                # readTh.start()
            else:
                imgjson = cam.takePicture()
                client.publish(topic="topic/img", payload=imgjson, qos=0, retain=False)
                time.sleep(0.04)
        else:
            upload_state = 0
            cam.releaseCam()
            cam = Camera(320, 240,160,120, json=True)
            
cam.releaseCam()   
client.loop_stop()
client.disconnect()  






