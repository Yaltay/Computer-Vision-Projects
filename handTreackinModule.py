import cv2
import mediapipe as mp
import time





class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.results = None
        self.tipIds = [4, 8, 12, 16, 20]
        self.img = None
        
    def findHands(self, img, draw = True):
        
        handsType = list()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)
        
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
                
        print(handsType)
        self.img = img
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        lmList = list()
        hand_label = None  # Elin sağ mı sol mu olduğunu depolayacak değişken
        
        if self.results.multi_hand_landmarks:
            
            # Hem el landmarklarını hem de elin sol/sağ bilgilerini alıyoruz
            for handNo, (handLms, handedness) in enumerate(zip(self.results.multi_hand_landmarks, self.results.multi_handedness)):
                # İlk tespit edilen elin landmarks verisi alınır
                myHand = self.results.multi_hand_landmarks[handNo]
                
                # Elin sol mu sağ mı olduğunu öğrenelim
                hand_label = handedness.classification[0].label  # 'Right' ya da 'Left' döner
                print(f"Tespit edilen el: {hand_label}")
    
                # Landmarkların koordinatlarını al
                for idd, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([idd, cx, cy])
    
                    # Landmarkları çiz
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                        
                
        """LeftTop = (lmList[4][1],lmList[12][2])
                RightBotton = (lmList[20][1],lmList[0][2])
                cv2.circle(img, (LeftTop), 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (RightBotton), 15, (0, 0, 255), cv2.FILLED)
                cv2.rectangle(img, (LeftTop),(RightBotton), (255,0,255),2)
                print(LeftTop)"""

                # Elin sol/sağ bilgisine göre görsel olarak farklılık ekleyebilirsiniz
        """ 
               if draw and hand_label == 'Right':
                    cv2.putText(img, "Sag El", (LeftTop[0] , LeftTop[1] -20 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif draw and hand_label == 'Left':
                    cv2.putText(img, "Sol El", (LeftTop[0] , LeftTop[1] -20 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        """
        return lmList, hand_label  # El listesiyle birlikte elin sağ mı sol mu olduğunu da döndürelim

                
     
            
    
            


    def AracHaraket(self,lmList):
        img = self.img
        sayac = 0
        if len(lmList) > 0:
            if lmList[20][2] < lmList[1][2]:
                    print("LMLİST: " , lmList[20][2] ,"   " ,lmList[1][2] )

                    for i in range(1, 5):
                        if lmList[self.tipIds[i]][2] < lmList[self.tipIds[i] - 2][2]:
                            sayac += 1
                    # 1 düzgit # 2 geri git # 0 dur # -1 saga don# -2 sola
                    if sayac > 3:  # El açık (ileriye git)
                      
                       
                      cv2.putText(img, f"Right Hand - Duz Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                     
                    else:  # El kapalı (geri git)
                        
                        cv2.putText(img, f"Right Hand - Geri Git", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 4)
                      
            else:
                if lmList[0][1] > lmList[13][1]:
                        
                    cv2.putText(img, f"Right Hand - saga don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                       
                else:
                       
                    cv2.putText(img, f"Right Hand - sola don", (10, 135), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 4)
                      
      


def main():
    
        
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    cap.set(3, 1260)
    cap.set(4, 1920)
    detector = handDetector()
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1) 
        
        img = detector.findHands(img)
        lmList , _ = detector.findPosition(img)
        detector.AracHaraket(lmList)
        
        if len(lmList) != 0:
            print((lmList[20]))
    
            
            

                        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        
        cv2.putText(img, str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,255),3)
        
        
        cv2.imshow("Image" , img)
        if  cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
    cv2.destroyAllWindows()


            
if __name__ == "__main__":
    main()
            
            