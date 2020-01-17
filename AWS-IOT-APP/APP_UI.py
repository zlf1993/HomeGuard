import tkinter as tk
import paho.mqtt.client as mqtt
import json
import sys
import threading
import cv2
from PIL import Image, ImageTk
import json
import codecs
import _pickle as cPickle
import numpy as np
import time


cafile = "./root-CA.crt"
cerfile = "./4a864e2ace-certificate.pem.crt"
keyfile = "./4a864e2ace-private.pem.key"
SERVER = "a37i47xeh8qin6-ats.iot.ca-central-1.amazonaws.com"
PORT = 8883
subscribe_list = [("topic/img", 0), ("$aws/things/BlackPi/shadow/update/accepted", 1),("topic/face", 1)]


people_number = 0
CameraState = 0
motion = "False"
temperature = "Not Get"
pedestrian = "0"
window = tk.Tk()
window.title("HomeAuto")
window.geometry('600x400')

angle_message = {
    "state": {
        "desired": {
            "angle":"90"
        }
    }
}
system_message = {
    "state": {
        "desired": {
            "system":"0"
        }
    }
}
camera_message = {
    "state": {
        "desired": {
            "camera":"1",
            "face":"0"
        }
    }
}
m_mes = json.dumps(camera_message)
face_message = {
    "state": {
        "desired": {
            "camera":"0",
            "face":"1"
        }
    }
}
f_mes = json.dumps(face_message)
basic_message = {
    "state": {
        "desired": {
            "camera":"0",
            "face":"0"
        }
    }
}
b_mes = json.dumps(basic_message)

def camera_state():
    global CameraState
    pro_state = CameraState
    # 1 try to turn off
    if pro_state:
        CameraState = 0
        system_message['state']['desired']['system'] = "0"
        s_mes = json.dumps(system_message)
        client.publish(topic='$aws/things/BlackPi/shadow/update', payload=s_mes, qos=1, retain=False)
        camera_button['text']="turn on"
    # 0 is off, try to turn on
    else:
        CameraState = 1
        cv2.destroyAllWindows()
        system_message['state']['desired']['system'] = "1"
        s_mes = json.dumps(system_message)
        client.publish(topic='$aws/things/BlackPi/shadow/update', payload=s_mes, qos=1, retain=False)
        camera_button['text']="turn off"
    cv2.destroyAllWindows()
    time.sleep(0.2)

def print_selection(v):
    angle_label.config(text='camera angle ' + v)
    angle = str(v)
    angle_message['state']['desired']['angle'] = angle
    g_mes = json.dumps(angle_message)
    client.publish(topic='$aws/things/BlackPi/shadow/update', payload=g_mes, qos=1, retain=False)

def print_radiobutton():
    mode_label.config(text='you have selected ' + var.get() + " Mode")
    if var.get() == "Basic":
        client.publish(topic='$aws/things/BlackPi/shadow/update', payload=b_mes, qos=1, retain=False)
    if var.get() == "Monitor":
        client.publish(topic='$aws/things/BlackPi/shadow/update', payload=m_mes, qos=1, retain=False)
    if var.get() == "Face":
        client.publish(topic='$aws/things/BlackPi/shadow/update', payload=f_mes, qos=1, retain=False)
    cv2.destroyAllWindows()
    time.sleep(0.2)

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))


def on_message(client, userdata, msg):

    if msg.topic == "$aws/things/BlackPi/shadow/update/accepted":
        # print(str(msg.payload))
        shadow = json.loads(msg.payload)
        if 'motion' in shadow['metadata']['desired'].keys():
            motion_timestamp = shadow['metadata']['desired']['motion']['timestamp']
            if motion_timestamp > client.motion_time:
                motion_state = shadow['state']['desired']['motion'].strip('\n').strip('\r')
                # print(motion_state)
                client.motion_time = motion_timestamp
                client.motion = motion_state
                motion_label.config(text="Motion Trigger:"+motion_state)
                #print("Motion Trigger:"+motion_state)
        if 'pedestrian' in shadow['metadata']['desired'].keys():
            pedestrian_timestamp = shadow['metadata']['desired']['pedestrian']['timestamp']
            if pedestrian_timestamp > client.pedestrian_time:
                pedestrian_state = str(shadow['state']['desired']['pedestrian'].strip('\n').strip('\r'));
                print(pedestrian_state)
                client.pedestrian_time = pedestrian_timestamp
                client.pedestrian +=1 
                people_label.config(text="Passed pedestrian number:"+str(client.pedestrian))
                print("Passed pedestrian number:"+pedestrian_state)
        if 'temperature' in shadow['metadata']['desired'].keys():
            temperature_timestamp = shadow['metadata']['desired']['temperature']['timestamp']
            if temperature_timestamp > client.temperature_time:
                temperature_state = str(shadow['state']['desired']['temperature'].strip('\n').strip('\r'));
                print(temperature_state)
                client.temperature_time = temperature_timestamp
                client.temperature = temperature_state
                temperature_label.config(text="Temperature:"+temperature_state)
                print("Temperature:"+temperature_state)
    if msg.topic == "topic/img":
        war_dic = json.loads(msg.payload)
        img_str = war_dic["state"]["desired"]["img"]
        #print(bytes2)
        img_bytes = bytes(img_str, encoding="gbk")
        img_b2 = codecs.escape_decode(img_bytes, 'hex-escape')[0]
        img_arr = cPickle.loads(img_b2)
        img_resize = cv2.resize(img_arr, (320,240), interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Image", img_resize)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destoryAllWindows()
        # img = Image.fromarray(img_arr)
        # image_file=ImageTk.PhotoImage(img)
    if msg.topic == "topic/face":
        print(msg.topic)
        face_dic = json.loads(msg.payload)
        face_str = face_dic["state"]["desired"]["face"]
        # print(bytes2)
        face_bytes = bytes(face_str, encoding="gbk")
        face_b2 = codecs.escape_decode(face_bytes, 'hex-escape')[0]
        face_arr = cPickle.loads(face_b2)
        face_resize = cv2.resize(face_arr, (320, 240), interpolation=cv2.INTER_CUBIC)
        face = Image.fromarray(face_resize)
        face_file=ImageTk.PhotoImage(face)
        canvas.create_image(0,0,anchor='nw',image=face_file)

frame = tk.Frame(window)
frame.pack()

frame_l = tk.Frame(frame)
frame_r = tk.Frame(frame)
frame_l.pack(side='left')
frame_r.pack(side='right')

people_label = tk.Label(frame_r, text="Passed pedestrian number:"+pedestrian,
                        bg='white', font=('Arial', 12), width=40, height=2)
motion_label = tk.Label(frame_r, text="Motion Trigger:"+motion,
                        bg='white', font=('Arial', 12), width=40, height=2)
temperature_label = tk.Label(frame_r, text="Temperature:"+temperature,
                        bg='white', font=('Arial', 12), width=40, height=2)

camera_button = tk.Button(frame_l, text="turn on", font=('Arial', 12), width=10, height=1, command=camera_state)
angle_label = tk.Label(frame_l, bg='green', font=('Arial', 12), fg='white', width=20, text='empty')
angle_scale = tk.Scale(frame_l, label='Angle', from_=30, to=150, orient=tk.HORIZONTAL, length=200, showvalue=0,
                       tickinterval=10, resolution=5, command=print_selection)
canvas = tk.Canvas(frame_r, bg='white', height=240, width=320)

var = tk.StringVar()
mode_label = tk.Label(frame_l, bg='yellow', font=('Arial', 12), width=30, text='Advanced Modes')
r1 = tk.Radiobutton(frame_l, text='Basic Mode', font=('Arial', 12), variable=var, value="Basic", command=print_radiobutton)
r2 = tk.Radiobutton(frame_l, text='Monitor Mode', font=('Arial', 12), variable=var, value="Monitor", command=print_radiobutton)
r3 = tk.Radiobutton(frame_l, text='Face Mode', font=('Arial', 12), variable=var, value="Face", command=print_radiobutton)

camera_button.pack()
people_label.pack()
motion_label.pack()
temperature_label.pack()
angle_label.pack()
angle_scale.pack()
canvas.pack()
mode_label.pack()
r1.pack()
r2.pack()
r3.pack()
# mqtt client setting
client = mqtt.Client(client_id="desktop", clean_session=True, userdata=None, transport="tcp")
client.tls_set(cafile, cerfile, keyfile)
client.ang_time = 0

client.motion_time = 0
client.motion = "False"
client.pedestrian_time = 0
client.pedestrian = 0
client.temperature_time = 0
client.temperature = "Lower than 28 degre"

client.canvas = canvas
client.window = window
client.on_connect = on_connect
client.on_message = on_message
client.connect(host=SERVER, port=PORT, keepalive=60, bind_address="")
client.loop_start()

s_mes = json.dumps(system_message)
client.publish(topic='$aws/things/BlackPi/shadow/update', payload=s_mes, qos=1, retain=False)
client.publish(topic='$aws/things/BlackPi/shadow/update', payload=b_mes, qos=1, retain=False)

client.subscribe(subscribe_list)

client.window.mainloop()
