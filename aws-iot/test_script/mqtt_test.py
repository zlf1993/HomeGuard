import paho.mqtt.client as mqtt
import json
import sys


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
    
    
client = mqtt.Client(client_id="mypc", clean_session=True, userdata=None, transport="tcp")
client.tls_set(cafile, cerfile, keyfile)
client.on_connect = on_connect
client.on_message = on_message

client.connect(host=SERVER, port=PORT, keepalive=60, bind_address="")
client.loop_start()

client.publish(topic=TOPIC, payload=Data_Out, qos=QOS, retain=False)




