import cv2
import numpy as np
from PIL import Image
import os
from cameraHelper import *
from voiceHelper import *



class TrainingHeler():
    # Path for face image database
    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = 0

    #def __init__(self):
    
    def startTraining(self):
        camHlpr = CameraHeler.getInstance()
        self.detector = camHlpr.getFaceCascade()
        speak("Training faces. It will take a few seconds. Wait.")        
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = self.getImagesAndLabels(self.path)
        camHlpr.recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        camHlpr.recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        
        speak("0 faces trained. Exiting Training".format(len(np.unique(ids))))
        
    # function to get the images and label data
    def getImagesAndLabels(self,path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids
