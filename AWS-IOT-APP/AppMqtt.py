import paho.mqtt.client as mqtt
import json
import sys
import threading
import cv2

TOPIC = "iot/topic"
message = {
    "state": {
        "desired":{
            "angle":"180"
        }
    }
}
Data_Out = json.dumps(message)
#print(Data_Out)
cafile = "./aws-iot/root-CA.crt"
cerfile = "./62c12da123-certificate.pem.crt"
keyfile = "./62c12da123-private.pem.key"
SERVER = "a37i47xeh8qin6-ats.iot.ca-central-1.amazonaws.com"
PORT = 8883
subscribe_list = [("topic/img",1),("$aws/things/BlackPi/shadow/update/accepted", 1),("$aws/things/BlackPi/shadow/get/accepted", 1)]

# static variable
organg_time_stamp = 0
    

# set read thread
readTh = threading.Thread(target = arser.readSerial)
readTh.setDaemon(True)
readTh.start()

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic)
    #if msg.topic == "$aws/things/BlackPi/shadow/update/accepted":
     #   print(str(msg.payload))
    if msg.topic == "$aws/things/BlackPi/shadow/update/accepted":
        print(str(msg.payload))
        shadow = json.loads(msg.payload)
        angle_timestamp = shadow['metadata']['angle']['timestamp']
        # tiemstap type int
        if angle_timestamp > client.ang_time:
            client.ang_time = angle_timestamp
            angle = shadow['state']['angle'].strip('\n').strip('\r')
            client.aser.writeSerial(bytes(angle, encoding="gbk"))
            # print(angle)
    if msg.topic == "topic/img":
        #print(str(msg.payload))
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
                #return a1
        
    #if msg.topic == "$aws/things/BlackPi/shadow/get/delta":
    #        print(str(msg.payload))

# set mqtt
client = mqtt.Client(client_id="", clean_session=True, userdata=None, transport="tcp")
client.tls_set(cafile, cerfile, keyfile)
client.ang_time = 0
client.aser = arser
client.on_connect = on_connect
client.on_message = on_message
client.connect(host=SERVER, port=PORT, keepalive=60, bind_address="")
client.loop_start()
client.subscribe(subscribe_list)
a = 1
while True:
    if arser.cameraState =="1":
        imgjson = cam.takePicture()
        # cv2.imshow("Image", img)
        key = cv2.waitKey(50)
        if key == 27:
            cv2.destroyAllWindows()
        # client.publish(topic="$aws/things/BlackPi/shadow/get", payload=(""), qos=1, retain=False)
        #if a ==1:
        #client.publish(topic="topic/img", payload=imgjson, qos=0, retain=False)
            #print("------++++++++")
        client.publish(topic="topic/img", payload=imgjson, qos=1, retain=False)
            # print(imgjson)
            #client.publish(topic="$aws/things/BlackPi/shadow/update", payload=imgjson, qos=1, retain=False)
            #a=2
    else:
        cv2.destroyAllWindows()
        
cam.releaseCam()   
client.loop_stop()
client.disconnect()   

# imgupload = Image2GoogleDrive()
# imgupload.upload()

    



# client.publish(topic="$aws/things/BlackPi/shadow/update", payload=Data_Out, qos=1, retain=False)




