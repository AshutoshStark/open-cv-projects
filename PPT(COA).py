import cv2
import os
from cvzone.HandTrackingModule import HandDetector

# var
width,height = 1280,720
folder_path = "E:\\iloveimg-resized"
imagenum = 0
buttonPress = False
counter = 0
Flipflop = 10
pen = [[]]
penNumber = -1
penStart = False

#Opticals
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(2,height)

# list of the presentaion list

pathImage =sorted(os.listdir(path = folder_path),key=len)
print(pathImage)

detector = HandDetector(detectionCon=0.2,maxHands=2 )
    

while True:
    # hand dectector 
    
    # for importing the images
    success,img = cap.read()
    img = cv2.flip(img,1)
    path_ppt = os.path.join(folder_path,pathImage[imagenum])
    imgcurrent = cv2.imread(path_ppt)
    gestureThreshold = 400
    
    #hand
    hands,img = detector.findHands(img)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),5)
    # operations
    
    if hands and buttonPress == False:
        hand = hands[0]
        handType = hand["type"]
        fingure1 = detector.fingersUp(hand)
        cx,cy = hand["center"]
        lmList = hand['lmList']
        
        #pointer projection
        indexFinger = lmList[8][0], lmList[8][1]
        # print(fingure1)

        if len(hands) == 2 :
            hand2 = hands[1]
            cx,cy = hand["center"]
            lmList2 = hand2['lmList']
            handType = hand2["type"]
            # print(fingure1)
        if cy <= gestureThreshold: # check the hight if the hand is at detection line or not
            #geusture of 1 - Left
            if fingure1 == [0,1,1,1,1] and handType == "Left":
                penStart = False
                buttonPress = True
                if imagenum < len(pathImage)-1:
                    pen = [[]]
                    penNumber = 0
                    imagenum +=1
                print("left")
            #geuseture of 2-Right
            if fingure1 == [0,1,1,1,1] and handType == "Right":
                buttonPress = True
                penStart = False
                if imagenum > 0 :
                    pen = [[]]
                    penNumber = 0
                    imagenum -=1
                print("Left")
        # Pointer on the ppt
        if fingure1 == [1,1,0,0,0] and handType == "Left":
            cv2.circle(imgcurrent,indexFinger, 12,(0,200,255),cv2.FILLED)
        # Draw on the ppt
        if fingure1 == [0,1,0,0,0] and handType == "Left":
            if penStart is False:
                penStart = True
                penNumber +=1
                pen.append([])
            cv2.circle(imgcurrent,indexFinger, 12,(0,200,255),cv2.FILLED)
            pen[penNumber].append(indexFinger)
        #Remove Drawing from the ppt
        if fingure1 == [1,1,1,0,0] and handType == "Right":
            if pen :
                if penNumber >=0:
                    pen.pop(-1)
                    penNumber -=1
                    buttonPress = True
            
    # this is to delay the slide change operation 
    if buttonPress == True :
        counter += 1
        if counter > Flipflop and buttonPress == True:
            counter = 0
            buttonPress = False
            
    # pen command or operation stored in it 
    for i in range (len(pen)) :
        for j in range (len(pen[i])):
            if j != 0:
                cv2.line(imgcurrent,pen[i][j-1],pen[i][j],(0,200,200),12)
                
    
    # the program will deploy the camra and the slides
    
    cv2.imshow("Image",img)
    cv2.imshow("slides",imgcurrent)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("a"):
        break
cv2.destroyAllWindows()