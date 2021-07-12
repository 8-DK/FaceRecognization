import cv2
import os
import time
import threading
from cameraHelper import *
import ctypes
from voiceHelper import *


# Define the thread that will continuously pull frames from the camera
class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()
        
    def get_id(self):    
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
            
class FaseDatasetHelper:            
    cam_cleaner = 0
    
    currentUseId = 0
    currentUerName = ""        
    
    def __init__(self):
        print("\n [INFO] FaseDatasetHelper init")
        self.camHlpr = CameraHeler.getInstance()                
    
    def startCapturing(self,userId,userName):
        speak("User Id "+str(userId)+", with User name "+userName+". is being register in database.")
        speak("Press S for save current progress. Press N for capture new image.")
        print("\n [INFO] User Id : "+str(userId)+", User name : "+userName)
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        count = 0
        captureImageFlag = 0
        self.cam_cleaner = CameraBufferCleanerThread(self.camHlpr.cam)
        while(True):    
            #ret, img = cam.read()
            if self.cam_cleaner.last_frame is not None:
                img = self.cam_cleaner.last_frame
                cv2.imshow('New Face', img)
                #img = cv2.flip(img, -1) # flip video image vertically
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = self.camHlpr.faceCascade.detectMultiScale(gray, 1.3, 5)
                keyPress  = 0
                for (x,y,w,h) in faces:
                    padding = 10
                    cv2.rectangle(img,(x-padding,y-padding),(x+w+padding,y+h+padding),(255,0,0),2)
                    if(captureImageFlag == 1):
                        cropFace = gray[y-padding:y+h+padding,x-padding:x+w+padding]
                        count += 1
                        # Save the captured image into the datasets folder        
                        captureFaceFileName = "dataset/User."+ str(userId) + '.' +  str(count) + ".jpg"
                        print("Capturing : "+captureFaceFileName)
                        cv2.imwrite(captureFaceFileName,cropFace)
                        #time.sleep(0.5)
                        captureImageFlag = 0
                    keyPress = cv2.waitKey(100) & 0xff                    
                    break;
                #cv2.imshow('image', img)
                
                if (keyPress  == 83) or (keyPress == 115): #s or S
                    print("S key pressed")
                    self.camHlpr.addUserToJson(userId,userName)
                    break
                elif (keyPress == 78) or (keyPress == 110): #n or N
                    print("N key pressed")
                    captureImageFlag = 1
                elif count >= 30: # Take 30 face sample and stop video
                     self.camHlpr.addUserToJson(userId,userName)
                     break    
        # Do a bit of cleanup
        cv2.destroyWindow("New Face")
        print("\n [INFO] Exiting Program and cleanup stuff")
        self.cam_cleaner.raise_exception()
        self.cam_cleaner.join()
        speak("User is registered in database.")
