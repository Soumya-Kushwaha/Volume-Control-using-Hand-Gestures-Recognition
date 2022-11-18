#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install opencv-python


# In[2]:


pip install pycaw


# In[3]:


import cv2
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# In[4]:


pip install --upgrade protobuf==3.20 --user


# In[5]:


pip install mediapipe --user


# In[6]:


import mediapipe as mp


# In[7]:


cap = cv2.VideoCapture(0) #for laptop's camera


# In[8]:


mpHands= mp.solutions.hands
hands = mpHands.Hands()
mpDraws = mp.solutions.drawing_utils
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


# In[9]:


while True:
    success, img= cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id, lm in enumerate (handLms.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int (lm.y*h)
                #print(id,cx,cy)
                lmList.append([id, cx, cy])
                #print(lmList)
            mpDraws.draw_landmarks(img , handLms , mpHands.HAND_CONNECTIONS)
        if lmList:
            x1 , y1 = lmList[4][1] , lmList[4][2]
            x2 , y2 = lmList[8][1] , lmList[8][2]
            cv2.circle(img , (x1 ,y1) ,15 , (255,0,255) ,cv2.FILLED)
            cv2.circle(img , (x2 ,y2) ,15 , (255,0,255) ,cv2.FILLED)
            cv2.line(img, (x1,y1) , (x2,y2) , (255 , 0, 255) ,3)
            
            z1 = (x1 + x2)//2
            z2 = (y1 + y2)//2
            
            cv2.circle(img , (z1,z2),15 ,(255,0,0) , cv2.FILLED )

            length = math.hypot(x2- x1 , y2- y1)
            #print(length)
            
            if length < 50:
                    cv2.circle(img , (z1 , z2) ,15 ,(255,255,255) , cv2.FILLED)
        vol = np.interp(length , [50 ,300] ,[minVol ,maxVol])
        volBar = np.interp(length , [50,300] ,[400 ,150])
        volPer = np.interp(length , [50 , 300] , [0,100])
        #print(vol)
        print(int(length) , vol)
        #print(volume.GetVolumeRange())
        volume.SetMasterVolumeLevel(vol, None)
        
        cv2.rectangle(img ,(50,150) , (85,400) ,(0,255,0) , 3)
        cv2.rectangle(img ,(50,int(volBar)) , (85,400) ,(0,255,0) , cv2.FILLED)
        cv2.putText(img , f'{int(volPer)}%', (40,450) ,cv2.FONT_HERSHEY_PLAIN,3 ,(0,255,255) ,3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)

