import cv2
import os
import time
import threading

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
cam = cv2.VideoCapture("rtsp://192.168.1.6:8554")

cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
#face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')#cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter user id end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
captureImageFlag = 0

# Define the thread that will continuously pull frames from the camera
class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()

class FaceDatasetHelper:

    cam_cleaner = CameraBufferCleanerThread(cam)
    currentUserId = 0
    currentUserInfo = ""
    
    def startDetecting(self,registerUuserID,userName):
        print("Press n to capture Image, Pres s to stop capturing")
        while(True):    
            #ret, img = cam.read()
            if cam_cleaner.last_frame is not None:
                img = cam_cleaner.last_frame
                cv2.imshow('image', img)
                #img = cv2.flip(img, -1) # flip video image vertically
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                k = 0
                for (x,y,w,h) in faces:
                    padding = 10
                    cv2.rectangle(img,(x-padding,y-padding),(x+w+padding,y+h+padding),(255,0,0),2)
                    if(captureImageFlag == 1):
                        cropFace = gray[y-padding:y+h+padding,x-padding:x+w+padding]
                        count += 1
                        # Save the captured image into the datasets folder        
                        captureFaceFileName = "dataset/User."+ str(face_id) + '.' +  str(count) + ".jpg"
                        print("Capturing : "+captureFaceFileName)
                        cv2.imwrite(captureFaceFileName,cropFace)
                        #time.sleep(0.5)
                        captureImageFlag = 0
                    keyS = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
                    break;
                #cv2.imshow('image', img)
                if (keyS == 115) or (keyS == 83): #s or S
                    break
                elif (keyS == 110) or (keyS == 83): # n or N
                    captureImageFlag = 1
                elif count >= 30: # Take 30 face sample and stop video
                     break    
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam_cleaner.join()
        cam.release()
        cv2.destroyAllWindows()
