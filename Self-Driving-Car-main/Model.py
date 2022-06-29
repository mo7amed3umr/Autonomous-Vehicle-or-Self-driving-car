from flask import Flask, request, Response
import time

import cv2
import numpy as np

import requests
from statistics import mode 
import sys
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from base64 import b64encode  
import os
import base64
import io
import cv2
from imageio import imread
import matplotlib.pyplot as plt
from flask_cors import CORS

PATH_TO_TEST_IMAGES_DIR = './images'

app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
   return Response({'Salma':14})

def lineDetection(img):  

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilation = cv2.dilate(edges, kernel, iterations = 1)

    lines = cv2.HoughLinesP(dilation,rho = 1,theta = 1*np.pi/180,threshold = 50,minLineLength = 100,maxLineGap = 100)  
    imgShape = img.shape
    return(lines,imgShape)
           
def select_rgb_white(image): 
    # white color mask  
    lower = np.uint8([200, 200, 200])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    masked = cv2.bitwise_and(image, image, mask = white_mask)
    return masked

           
def linesPositions(image,houghimage):
    masked = select_rgb_white(image)
    lines,imgShape = lineDetection(masked)
    line_dict = {'left':[], 'right':[]}
    img_center = imgShape[1]//2
    if (lines is not None):
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1<img_center and x2<img_center:
                    position = 'left'

                elif x1>img_center and x2>img_center:
                    position = 'right'

                else:
                    continue
                line_dict[position].append(np.array([x1, y1]))
                line_dict[position].append(np.array([x2, y2]))
                cv2.line(houghimage,(x1,y1),(x2,y2),(0,255,0), 2)

    return(line_dict,houghimage)

def DirectionOfTheCar(image):
#     image = cv2.imread(imgPath)
#     count = count + 1
    houghLinesImage = np.zeros_like(image) 
    positionOfTheLine ,finalimage= linesPositions(image,houghLinesImage)
#     cv2.imwrite("finalimage.jpeg",finalimage)

    left,right = len(positionOfTheLine['left']),len(positionOfTheLine['right'])

    direction={''}

    if((np.abs(left-right) <= 8)):
        direction ={'forward'}
       
    elif(left > right):
        direction = {'right'}
        
    elif(right > left):
        direction = {'left'}
    else:
        direction = {'stop'}
    return(direction,finalimage)
@app.route("/image", methods=["POST"])
def image():

    i = request.files.get('image',None) # get the image
    f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    
    i.save('%s' % ( f))

    frame = imread(f)

    frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0, 
                        interpolation = cv2.INTER_CUBIC) 

    DirectionSendToServer,imageAfterLineDetection = DirectionOfTheCar(frame[100:,:,:])
    cv2.imwrite("finalimage.jpeg",imageAfterLineDetection)

    print(DirectionSendToServer, flush=True)

    return Response("%s saved" % f)



       
      
   

    
if __name__ == '__main__':
    app.run(debug=True, host='localhost')