import serial
import threading
import time
import os
class ArduinoSerial:
    def __init__(self, path='/dev/ttyACM0'): 
        assert os.path.exists(path)
        self.ser = serial.Serial(path, 9600, timeout=1);
        self.cameraState = "0"
        self.motion = "2"
        self.pedestrian = "0"
        self.temperature = "0" #low 5    high 4

    def writeSerial(self, value):
        # serial.write() only support bytes
        self.ser.write(value);
        
    def readSerial(self):
        while True:
            b = self.ser.read(3)
            # print(b)
            s1 = str(b, encoding = 'utf-8').strip('\n').strip('\r')
            if s1 != "":
                print(s1)
                if s1 == "1" or s1 == "0":
                    self.cameraState = s1
                elif s1 == "2" or s1 == "3":
                    self.motion = s1
                elif s1 == "5" or s1 == "4":
                    self.temperature = s1
                elif s1 == "6":
                    print("pedestrian"+s1)
                    self.pedestrian = s1
                elif s1 == "7":
                    #print("gone"+s1)
                    self.pedestrian = s1
            time.sleep(0.5);
        
    def release(self):
        self.ser.close();
        
if __name__ == "__main__":
    arser = ArduinoSerial()
    writeTh = threading.Thread(target = arser.writeSerial(8))
    readTh = threading.Thread(target = arser.readSerial)
    threads = [writeTh, readTh]
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()