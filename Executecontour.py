import cv2 
import numpy as np 

frame_with = 640 
frame_hight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frame_with)
cap.set(4, frame_hight)



def onChange(a):
    pass

window_name = "Parameters"
cv2.namedWindow("Parameters")
cv2.resizeWindow(window_name, (640,240))
cv2.createTrackbar('Threshold1', window_name, 26, 255, onChange)
cv2.createTrackbar('Threshold2', window_name, 47, 255, onChange)




def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver



def get_contour(img,imgContour):
    
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area > 1000:
            cv2.drawContours(imgContour, cnt, -1, (0, 255, 0), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri , True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect((approx))
            cv2.rectangle(imgContour, (x,y),(x+w,y+h), (0,0,255),5)
            cv2.putText(imgContour, "Kose Sayisi " + str(len(approx)), (x+w+30 , y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0),2)
            

        




while True:
    ret ,img = cap.read()
    imgContour = img.copy()
    
    gausian_img = cv2.GaussianBlur(img, ksize = (7,7), sigmaX = 1)
    gray_image = cv2.cvtColor(gausian_img, cv2.COLOR_BGR2GRAY)
    
    
    threshold1 = cv2.getTrackbarPos("Threshold1", window_name)
    threshold2 = cv2.getTrackbarPos("Threshold2", window_name)

    
    img_canny = cv2.Canny(gray_image,threshold1,threshold2)
    
    
    karnel = np.ones((5,5))
    img_dilate = cv2.dilate(img_canny, karnel)
    
    get_contour(img_dilate, imgContour)
    
    stack_image = stackImages(0.8, ([img,img_canny,gray_image],
                                    [img_dilate,imgContour,imgContour]))
    
    cv2.imshow("pencere", stack_image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    

cv2.destroyAllWindows()
