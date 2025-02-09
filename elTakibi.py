import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


pTime = 0
cTime = 0




while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for idd,lm in enumerate(handLms.landmark):
                print("ID: " ,idd , "LM: ",lm)
                h ,w ,c = img.shape
                cx ,cy = int(lm.x * w) , int(lm.y * h)
                print(idd , cx , cy )
                if idd==0:
                    cv2.circle(img, (cx,cy),20,(0,0,0), cv2.FILLED)
                    
                if idd==20:
                    cv2.circle(img, (cx,cy),20,(255,0,0), cv2.FILLED)
                if idd==4:
                    cv2.circle(img, (cx,cy),20,(255,0,0), cv2.FILLED)
                
                
                
            mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
            
            
            
     
            
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    
    
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255),3)
    
    
    cv2.imshow("Image", img)
    if  cv2.waitKey(1) & 0xFF == ord("q"):
        break
            


cv2.destroyAllWindows()
            
            
            