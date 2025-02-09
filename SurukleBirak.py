import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

colorR = (255,0,255) 

cx , cy , w ,h  = 100,100,200,200




class DragRect():
    def __init__(self,posCenter,color = (255,0,255),size=[200,200]):
        self.posCenter = posCenter
        self.size = size
        self.color = color
        
        
        
    def update(self,cursor):
        cx ,cy = self.posCenter
        w,h = self.size
            
            
        if cx - w // 2< cursor[0]  <cx + w//2 and cy - h //2 < cursor[1] < cy +  h//2:
            
            
            self.color = 0,255,255    
            self.posCenter = cursor
        else:
            self.color = 0,0,255
            
                
            



rect_list = []

for x in range(5):
    rect_list.append(DragRect([x*250 +150 ,150]))
    

while True:
    success , img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    
    lmList , _ = detector.findPosition(img)
    if lmList:
        
        
        lenght , _ , _  = detector.findDistance(8, 12, img) #♠ bu fonksiyon işaret ile orta parmak arasında mesafeyi dondurur 
        # _ 1.si çizilmiş resmi dönürür   _ 2. si ise 1. ve 2. parmağın noktalarını ve orta naktonanın kordinatlarını dondurur.
        print(lenght)
        if lenght < 40 :
            
            cursor = lmList[8]
            
            for rect in rect_list:
                rect.update(cursor)
            
        
        
    for rect in rect_list:
        color = rect.color
        cx ,cy = rect.posCenter
        w , h = rect.size
        
        cv2.rectangle(img, (cx-w//2 , cy - h//2),(cx+w//2 , cy + h//2), color ,cv2.FILLED)
        cvzone.cornerRect(img, (cx-w//2 , cy - h//2 , w,h),15,rt=0)
    
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
cv2.destroyAllWindows()


