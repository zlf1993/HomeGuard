import cv2

cap = cv2.VideoCapture(0)
while True:
    et, img = cap.read()
    print(et)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cv2.destroyAllWindows()
cam.releaseCam()
        
