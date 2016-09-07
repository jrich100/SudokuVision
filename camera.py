import cv2
import sys
import time
import os
import numpy as np

class Camera(object):
    
    cam          = None
    intr_matrix  = None
    dist_coefs   = None
    
    
    def __init__(self, cam_input):
        self.cam = cv2.VideoCapture(cam_input)
        if not self.cam.isOpened(): raise "Unable to Access Camera"
    
    
    def calibrate(self, img_names):
        if not img_names: return False
        
        pattern_size = (9, 6)
        pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
        pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    
        obj_points = []
        img_points = []
        h, w = 0, 0
        for fn in img_names:
            
            img = cv2.imread(fn, 0)
            if img is None:
              print "Failed to load", fn
              continue
    
            h, w = img.shape[:2]
            found, corners = cv2.findChessboardCorners(img, pattern_size)
            if found:
                term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
            
            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)
    
        rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,
                                                                       (w, h), None, None)
        #print 'Calibration reprojection error: '+ str(rms)
        
        self.intr_matrix = camera_matrix
        self.dist_coefs = dist_coefs
    
    def getFrame(self):
        ret, frame = self.cam.read()
        if ret: return frame
        else: raise "Lost Connection to Camera"
    
    def getFramePair(self):
        ret1, frame1 = self.cam.read()
        ret2, frame2 = self.cam.read()
        if ret1 or ret2: return frame1, frame2
        else: raise "Lost Connection to Camera"
    
    def close(self):
        self.cam.release()



    
def loop():
   
    MIN_CONTOUR_AREA = 100
    background = None
    alarm = False
    rec = False
    
    i = 0
    while True:
        t = time.time()
        ret, frame = cam.read()
        
        # if the first frame is None, initialize it
        if ((int(t) % 1000) == 0 or background is None) and alarm == False:
            print 'background refreshed: '+str(time.strftime("%I:%M:%S"))
            background = frame.copy()
        
        
        # convert to grayscale, and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(gray, (21, 21), 0)
        
        grayb = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        imgb = cv2.GaussianBlur(grayb, (21, 21), 0)
        
        # compute the absolute difference between the current frame and
        # first frame
        diff = cv2.absdiff(imgb, img)
        thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((5,5),np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=4)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        # loop over the contours
        found = None
        for c in cnts[1]:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < MIN_CONTOUR_AREA:
                    continue
            found = c
            alarm = True
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        if found is None:
            alarm = False
            if rec:
                rec = False
                out.release()
                "saved video: " + str(i) 
        else:
            if i == 0:
                rec = True
                i+=1
            if not rec:
                i+=1
                print 'starting video: ' + str(i)
                out = cv2.VideoWriter(newpath +'video'+str(i)+'.avi', -1, 25, (640, 480));
                rec = True
                
                
        
        
        message, col = ("[WARNING]", (0,0,255)) if alarm  else ("[CLEAR]", (0,255,0))
        
        cv2.putText(frame, message, (40,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, col, 1)
        
        # Display the resulting frame
        cv2.imshow('combine', cv2.addWeighted(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR), .4,
                                              frame, .6, 0))
        cv2.imshow('Video', frame)
        
        #save video
        if rec: out.write(frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            print "saved video: " + str(i) 
            out.release()
            break
    
    # When everything is done, release the capture
    cam.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    cam_input = 1
    
    cam = cv2.VideoCapture(cam_input)
    
    while True:
        ret, frame = cam.read()
        
        cv2.imshow('Video', frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
        
    cam.release()
    cv2.destroyAllWindows()
        
    
    
