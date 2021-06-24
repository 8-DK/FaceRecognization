import cv2
import numpy as np
import os
from cameraHelper import *
from face_dataset_helper import *
from face_training_helper import *
from voiceHelper import *

CameraUrl = "rtsp://192.168.1.45:5554"
TrainingFilPath = "trainer/trainer.yml"

camHelper = CameraHeler(CameraUrl,TrainingFilPath)
datasetHlpr = FaseDatasetHelper()
trainingHlpr = TrainingHeler()

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
        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = camHelper.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                id = camHelper.userNames[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), camHelper.font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), camHelper.font, 1, (255,255,0), 1)              
        
        resize = camHelper.ResizeWithAspectRatio(img, width=300)
        cv2.imshow('camera',resize) 

        keyPress = chr(cv2.waitKey(10) & 0xff) # Press 'ESC' for exiting video        
        if (keyPress == 't') or (keyPress == 'T'): #start training
            speak("Start data set training. Please wait while training is completed.")
            trainingHlpr.startTraining()
            break
        if (keyPress == 'c') or (keyPress == 'C'): #capture new photo
            speak("Inter name of new user, who you wish to register.")
            val = input("Inter name of new user -> ")
            datasetHlpr.startCapturing(camHelper.lastUserId,val)

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    camHelper.release()    

if __name__ == "__main__":
    main()