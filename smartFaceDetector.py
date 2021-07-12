import cv2
import numpy as np
import os
import time
from cameraHelper import *
from face_dataset_helper import *
from face_training_helper import *
from voiceHelper import *

CameraUrl = "rtsp://192.168.1.45:5554"
TrainingFilPath = "trainer/trainer.yml"

#camHelper = CameraHeler(CameraUrl,TrainingFilPath)
camHelper = CameraHeler(0)

datasetHlpr = FaseDatasetHelper()
trainingHlpr = TrainingHeler(TrainingFilPath)

def main():
    speak("Welcome to smart doorbell")
    camHelper.loadUserInfo()
    while True:
        ret, img = camHelper.cam.read()
        #img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = camHelper.faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(camHelper.minW), int(camHelper.minH)),
           )

        detectedPersons = []
        lastUserDetected = ""
        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id = -1
            confidence = 100
            if(camHelper.isTrainingFilePresent):
                id, confidence = camHelper.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            print("Current user id:"+str(id))
            if (confidence < 100):
                if(len(camHelper.userNames)):                    
                    lastUserDetected = camHelper.userNames[id-1]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = -1
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, lastUserDetected, (x+5,y-5), camHelper.font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), camHelper.font, 1, (255,255,0), 1)              
        
        if(lastUserDetected  != "unknown") and (lastUserDetected  != "" and (id != -1)):
            print(str(time.time()-camHelper.getLastVisitedTime(id,lastUserDetected)))
            if( (time.time()-camHelper.getLastVisitedTime(id,lastUserDetected)) > 5):            
                camHelper.setLastVisitedTime(id,time.time())
                speak("Welcome "+lastUserDetected )
        
        resize = camHelper.ResizeWithAspectRatio(img, width=300)
        cv2.imshow('camera',resize) 

        keyPress = chr(cv2.waitKey(10) & 0xff) # Press 'ESC' for exiting video        
        if (keyPress == 't') or (keyPress == 'T'): #start training
            speak("Start data set training. Please wait while training is completed.")
            trainingHlpr.startTraining()            
        if (keyPress == 'c') or (keyPress == 'C'): #capture new photo
            speak("Enter name of new user, who you wish to register.")
            val = input("Inter name of new user -> ")
            if(val != ""):
                datasetHlpr.startCapturing(camHelper.lastUserId,val)
            else:
                speak("No name enterd.")

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    camHelper.release()    

if __name__ == "__main__":
    main()