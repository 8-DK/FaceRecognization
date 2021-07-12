import cv2
import numpy as np
import os
import json
from os.path import exists

class CameraHeler:
    cam = 0
    recognizer = 0
    mCameraUrl = ""
    mTrainingFilePath = ""
    faceCascade = 0    
    font = 0    
    minW = 0
    minH = 0
    userInfo = []
    userNames = []
    userIds = []
    processThisId =[]
    lastUserId = 1;
    isTrainingFilePresent = 0
    
    __shared_instance = 'cameraHelper'
  
    @staticmethod
    def getInstance():
        """Static Access Method"""
        if CameraHeler.__shared_instance == 'cameraHelper':
            CameraHeler("rtsp://192.168.1.45:5554","trainer/trainer.yml")
        return CameraHeler.__shared_instance
    
    def __init__(self,cameraID = -1,cameraUrl = "rtsp://192.168.1.45:5554" ,trainingFilePath = "trainer/trainer.yml"):
        
        """virtual private constructor"""
        if CameraHeler.__shared_instance != 'cameraHelper':
            raise Exception ("This class is a singleton class !")
        else:
            CameraHeler.__shared_instance = self
        
        self.loadUserInfo()
        
        self.mCameraUrl = cameraUrl
        self.mTrainingFilePath = trainingFilePath
        
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        if(exists(self.mTrainingFilePath)):
            self.recognizer.read(self.mTrainingFilePath)
            self.isTrainingFilePresent = 1
        else:
            self.isTrainingFilePresent = 0

        self.faceCascade =  cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");
        self.font = cv2.FONT_HERSHEY_SIMPLEX        
        # Initialize and start realtime video capture
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
        if(cameraID > -1):
            self.cam = cv2.VideoCapture(0)
        else:
            self.cam = cv2.VideoCapture(self.mCameraUrl)
        #cam = cv2.VideoCapture(0)
        self.cam.set(3, 640) # set video widht
        self.cam.set(4, 480) # set video height

        # Define min window size to be recognized as a face
        self.minW = 0.1*self.cam.get(3)
        self.minH = 0.1*self.cam.get(4)
        
    def updateTrainingFile(self):
        self.recognizer.read(self.mTrainingFilePath)
        self.isTrainingFilePresent = 1
    
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
                self.lastUserId = 1
                for userData in self.userInfo:
                    self.lastUserId += 1
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
    
    def getLastVisitedTime(self,userId,userName = ""):
        print("getLastVisitedTime for User id : "+str(userId))
        print(str(self.userInfo))
        print("\n")
        if(len(self.userInfo) > (userId-1)):
            if(self.userInfo[userId-1]['userName'] == userName):
                if self.userInfo[userId-1].__contains__('lastVisiteTime'):
                    return self.userInfo[userId-1]['lastVisiteTime']
                return 0

        for usrInfo in self.userInfo:
            if(usrInfo['userName'] == userName):
                if usrInfo.haskey('lastVisiteTime'):
                    return usrInfo['lastVisiteTime']
                return 0
        return 0
    
    def setLastVisitedTime(self,userId,mTime):
        print("setLastVisitedTime for User id : "+str(userId)+" New time:"+str(mTime))
        print(str(self.userInfo))
        if(self.userInfo[userId-1]['id'] == userId):
            if self.userInfo[userId-1].__contains__('lastVisiteTime'):                
                self.userInfo[userId-1]['lastVisiteTime'] = mTime
        self.userInfo[userId-1].update({"lastVisiteTime":mTime})
        print(str(self.userInfo))

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

