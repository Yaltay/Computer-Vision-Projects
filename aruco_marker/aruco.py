import cv2
import cv2.aruco as aruco
import numpy as np
import os



def findArucoMarkers(img,markesSize = 6, totalMarkers = 250 , draw = True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markesSize}X{markesSize}_{totalMarkers}')
    print(key)
    arucoDict = aruco.getPredefinedDictionary(key)
    arucoParam = aruco.DetectorParameters()
    bboxs , ids ,rejected =  aruco.detectMarkers(imgGray, arucoDict,parameters=arucoParam)

    print(ids)
    
    if draw:
        aruco.drawDetectedMarkers(img, bboxs,borderColor=(0,0,255))
        print(bboxs[0][0][0][0])
        a = int(bboxs[0][0][0][0])
        b = int(bboxs[0][0][0][1])
        #cv2.circle(img, (a,b), 10, (255,0,0),cv2.FILLED)        
    return [bboxs , ids]



def augmentAruco(bbox ,idd,img,imgAug,drawID = True):
    
    tl = bbox[0][0][0] , bbox[0][0][1]
    tr = bbox[0][1][0] , bbox[0][1][1]
    br = bbox[0][2][0] , bbox[0][2][1]
    bl = bbox[0][3][0] , bbox[0][3][1]
    
    h ,w, c = imgAug.shape
    
    pts1 = np.array([tl,tr,br,bl])
    pts2 = np.float32([[0,0],[w,0],[w,h],[0,h]])
    
    matrix , _ = cv2.findHomography(pts2, pts1)
    imgOut = cv2.warpPerspective(imgAug, matrix,(img.shape[1],img.shape[0]))
    cv2.fillConvexPoly(img, pts1.astype(int), (0,0,0))
    imgOut = img +imgOut
    
    
    
    tl_int = tuple(int(x) for x in tl)

    if drawID:
        
        cv2.putText(imgOut,str(idd) , tl_int, cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale = 3, color = (255,0,255),thickness=3)
    
    
    
    
    
    
    
    return imgOut



def main():
    img = cv2.imread("markers.jpg")
    arucoFound = findArucoMarkers(img)
    imgAug = cv2.imread("23.jpg")
   
    while True:
        
        if len(arucoFound[0]) != 0:
            for bbox , idd in zip(arucoFound[0],arucoFound[1]):
                img = augmentAruco(bbox, idd, img, imgAug)
        
        
        
        
        
        cv2.imshow("winname",img)
        cv2.waitKey(10) 
        
    




if __name__ == "__main__":
    main()







