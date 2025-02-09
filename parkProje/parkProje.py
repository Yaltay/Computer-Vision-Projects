import cv2
import cvzone 
import pickle







width ,height = 107 , 48

try:
    with open("CarParkPos" , "rb") as f:
        posList = pickle.load(f)
except:
    posList = list()




count = 0


def mouseClick(event, x, y, flags, param):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i , pos in enumerate(posList):
            x1 , y1 = pos
            if x1 < x < x1+ width and y1 < y < y1 + height:
                posList.pop(i)
        
    with open("CarParkPos" , "wb") as f:
        pickle.dump(posList, f)



while True:
    img = cv2.imread("carParkImg.png")

    for pos in posList:
        cv2.rectangle(img, pos , (pos[0] + width , pos[1] + height) , (255,0,0) , 2)
    cv2.imshow("IMG", img)
    cv2.setMouseCallback("IMG", mouseClick)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()