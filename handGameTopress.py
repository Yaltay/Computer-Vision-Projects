import cv2 
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import random
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)


detector = HandDetector(detectionCon=0.8,maxHands=1)

#find function 
# x pixel olarak mesafedir   y is gerçek santimetre dir kamera ile elimizdeki

x = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
y = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]

coff = np.polyfit(x, y, 2)
print(coff)

counter = 0 

cx , cy = 250,250

color = ( 255,0,255)
score = 0

timeStart = time.time()
totalTime = 20

while True:
    suc , img = cap.read()
    img = cv2.flip(img, flipCode = 1)
    hands = detector.findHands(img,draw=False)
    
    if time.time() - timeStart < totalTime:

    
        if (len(hands)) != 0:
            lmList = hands[0]["lmList"]
            x ,y,w,h = hands[0]["bbox"]
            
            
                
            x1 , y1 = lmList[5]
            x2 , y2 = lmList[17]    
            
            distance =int( math.sqrt( (y2-y1)**2  + (x2-x1)**2))
            
            A , B , C = coff
            distanceCm = A*distance**2 + B*distance + C
            
            
            if distanceCm < 40:
                if x < cx < x+w and y < cy <y+h:
                    counter = 1
                    
            cvzone.putTextRect(img, f'{int(distanceCm)} cm',(x,y) )
            cv2.rectangle(img, (x,y),(x+w,y+h), (0,0,0),3)
        
        if counter:
            counter+=1
            color = (0,255,0)
            if counter == 3:
                cx = random.randint(100, 1000)
                cy = random.randint(100, 600)
                color = (255,0,255)
                score += 1 
                counter = 0
                
        
        
        print(cx)
        
        cv2.circle(img,  (cx,cy), 30 ,   color , cv2.FILLED)
        cv2.circle(img,  (cx,cy), 20 ,   (255,255,255) , cv2.FILLED)
        cv2.circle(img,  (cx,cy), 10 ,   (0,0,0) , cv2.FILLED)
    
        cvzone.putTextRect(img, f'Time : {int(totalTime -(time.time() -timeStart))}', (1000,55), scale=3)
        cvzone.putTextRect(img, f'Score : {score}', (60,55), scale=3)
        
    
    else:
        cvzone.putTextRect(img, "Oyun Bitti  ", (400,400), scale=3 ,offset=30 , thickness=7)
        cvzone.putTextRect(img, f'Score : {score}', (450,500), scale=3 ,offset=30 , thickness=7)
        cvzone.putTextRect(img, "Oyuna Tekrar baslamak icin r Tusuna basin", (250,600), scale=2 ,offset=20 , thickness=5)

    
    
    
    cv2.imshow("winname", img)
    key = cv2.waitKey(1)
    
    if key  == ord("q"):
        break
    elif key == ord("r"):
        timeStart = time.time()
        score = 0

cv2.destroyAllWindows()














