import cv2 
import numpy as np 

frame_with = 640 
frame_hight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frame_with)
cap.set(4, frame_hight)




while True:
    timer = cv2.getTickCount()
    succses , img = cap.read()
    
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),3)
    roi = cv2.selectROI("ROI Selection", img, showCrosshair=True, fromCenter=False)
    x ,y ,w ,h = roi
    print(x,y,w,h)
    
    roi_cropped = img[y:y+h, x:x+w]

    
    cv2.imshow("Selected ROI", roi_cropped)
    
    
    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
