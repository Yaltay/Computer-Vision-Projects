import cv2
import cvzone 
import pickle
import numpy as np

cap = cv2.VideoCapture("carPark.mp4")
width ,height = 107 , 48

with open("CarParkPos" , "rb") as f:
     posList = pickle.load(f)
     
     
     
     
     
     
     
def ParkYeriKontrol(imgPros):
    bosYerSayisi = 0

    for pos in posList:
        x , y = pos
        imgCrop = imgPros[y:y+height , x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x , y + height -5 ) , scale=1 , thickness= 2 ,offset=0)
        
        if count < 800:
            renk = (255,0,0)
            kalinlik = 5
            bosYerSayisi += 1
        else:
            renk = (0,0,255)
            kalinlik = 2

        cv2.rectangle(img, pos , (pos[0] + width , pos[1] + height) , renk , kalinlik)
    cvzone.putTextRect(img, f'Bos yer sayisi: {bosYerSayisi}/ {len(posList)} ', (100,50 ) , scale=3 , thickness= 3 ,offset=10)

        
while True:
    
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
    _ , img = cap.read()
    imgGray = cv2.cvtColor(img, code = cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, ksize = (3,3), sigmaX = 1)
    imgThresHold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)
    imgMedian = cv2.medianBlur(imgThresHold, (5))
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3),np.uint8))
    
    
    
    ParkYeriKontrol(imgDilate)
        
    cv2.imshow("IMG", img)
    cv2.imshow("imgThresHold", imgThresHold)
    cv2.imshow("imgMedian", imgMedian)
    cv2.imshow("imgDilate", imgDilate)

    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()