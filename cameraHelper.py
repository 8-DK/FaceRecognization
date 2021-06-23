import cv2
import numpy as np
import os
import json

class CameraHeler:
    cam = 0
    recognizer = 0
    mCameraUrl = ""
    mTrainingFilePath = ""
    faceCascade = 0    
    font = 0    
    minW = 0
    minH = 0
    userInfo = {}
    userNames = []
    userIds = []
    lastUserId = 1;
    
    __shared_instance = 'cameraHelper'
  
    @staticmethod
    def getInstance():
        """Static Access Method"""
        if CameraHeler.__shared_instance == 'cameraHelper':
            CameraHeler("rtsp://192.168.1.45:5554","trainer/trainer.yml")
        return CameraHeler.__shared_instance
    
    def __init__(self,cameraUrl = "rtsp://192.168.1.45:5554" ,trainingFilePath = "trainer/trainer.yml"):
        
        """virtual private constructor"""
        if CameraHeler.__shared_instance != 'cameraHelper':
            raise Exception ("This class is a singleton class !")
        else:
            CameraHeler.__shared_instance = self
        
        self.loadUserInfo()
        
        self.mCameraUrl = cameraUrl
        self.mTrainingFilePath = trainingFilePath
        
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(trainingFilePath)

        self.faceCascade =  cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");
        self.font = cv2.FONT_HERSHEY_SIMPLEX        
        # Initialize and start realtime video capture
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        self.cam = cv2.VideoCapture(self.mCameraUrl)
        #cam = cv2.VideoCapture(0)
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        self.minW = 0.1*self.cam.get(3)
        self.minH = 0.1*self.cam.get(4)
        
    def predict(self, faceImg):
        return self.recognizer.predict(faceImg)
    
    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()
        
    def getFaceCascade(self):
        return self.faceCascade
        
    def getCamera(self):
        return self.cam

    def loadUserInfo(self):
        if os.path.exists("userData.json"):
            f = open('userData.json',)
            try:
                self.userInfo = json.load(f)['users']
                lastUserId = 1
                for userData in self.userInfo:
                    lastUserId += 1
                    print(userData)
                    self.userNames.append(userData.get("userName"))
                    self.userIds.append(userData.get("id"))
            except:
                print("invalid json")
                
    def addUserToJson(self,userId,userName):
        self.userNames.append(userId)
        self.userIds.append(userName)
        outDict = {}    
        self.userInfo.append({"userName":userName,"id":userId})
        outDict = {'users':self.userInfo}
        with open("userData.json", "w") as outfile: 
            json.dump(outDict, outfile)
        self.loadUserInfo()

    def ResizeWithAspectRatio(self,image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

            return cv2.resize(image, dim, interpolation=inter)

