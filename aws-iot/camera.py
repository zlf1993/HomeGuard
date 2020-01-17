import cv2
import numpy as np
from PIL import Image
import json
import _pickle as cPickle
import codecs
import os
import time

class Camera:
    def __init__(self, width, height, resize_w, resize_h, json=True, path="/home/pi/Documents/aws-iot/Image/CameraFrame.jpeg"):
        self.json = json
        self.path = path
        self.w = resize_w
        self.h = resize_h
        try:
            self.cap = cv2.VideoCapture(0)
        except cv2.error as e:
            print(e, " can not capture camera0.")
        except:
            print("unknown error.")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # self.cap.set(cv2.CAP_PROP_FPS, fps)
    def savePicture(self):
        ret, frame = self.cap.read()
        if ret == True :
            if os.path.exists(self.path):
                os.remove(self.path)
            cv2.imwrite(self.path,frame)
            
    def takePicture(self):
        ret, frame = self.cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_resize = cv2.resize(frame_gray, (self.w, self.h), interpolation=cv2.INTER_CUBIC)
        if ret == True :
            #if os.path.exists(self.path):
            #    os.remove(self.path)
            #cv2.imwrite(self.path,frame)
            # opencv read result is np.array format, PIL is PIL.Image format
            if self.json == True :
                dic = {
                    "state": {
                        "desired":{
                            "img": None
                        }
                    }
                }
                bytesImg = cPickle.dumps(frame_resize)
                strImg = s = str(bytesImg)[2:-1]
                dic["state"]["desired"]["img"] = strImg
                dicJson = json.dumps(dic)
                #war_dic = json.loads(dicJson)
                #bytes2 = war_dic["state"]["desired"]["img"]
                #print(bytes2)
                #b1 = bytes(bytes2, encoding="gbk")
                #b2 = codecs.escape_decode(b1, 'hex-escape')[0]
                #a1 = cPickle.loads(b2)
                #return a1
                return dicJson
            return frame
        return None
    
    def releaseCam(self):
        self.cap.release()

if __name__ == "__main__":
    cam = Camera(320, 240, 160, 120, True)
    #img = cam.takePicture()
    #cv2.imshow("Image", img)
    #key = cv2.waitKey(30)
    while True:
        # et, img = cam.cap.read()
        img = cam.takePicture()
        
        war_dic = json.loads(img)
        bytes2 = war_dic["state"]["desired"]["img"]
        b1 = bytes(bytes2, encoding="gbk")
        b2 = codecs.escape_decode(b1, 'hex-escape')[0]
        a1 = cPickle.loads(b2)
        cv2.imshow("Image", a1)
        key = cv2.waitKey(30)
        if key == 27:  
            cv2.destroyAllWindows()
            cam.releaseCam()
        
