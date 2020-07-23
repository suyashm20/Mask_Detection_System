# -*- coding: utf-8 -*-
"""mask_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sp80MfS3sOJHeZAJC-nEKurN6Ei1GJ5Q
"""

import cv2
import os
from keras.models import load_model
import numpy as np
import time
from google.colab.patches import cv2_imshow


frame = cv2.imread('photo.jpg', cv2.IMREAD_UNCHANGED)
# frame = cv2.resize (frame, (800,640))
cv2_imshow(frame)
    
  


face = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

lbl=['No Mask','Mask']

model = load_model('cnn_150.h5')

path = os.getcwd()
#cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    
height,width = frame.shape[:2] 
print(height,width)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))  ## CLAHE for contrast settings
gray = clahe.apply(gray)
# gray = cv2.equalizeHist(gray)
cv2_imshow(gray)
    
faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
   


for (x,y,w,h) in faces:
       
  face_1 = frame[y:y+h , x:x+w] 
  face_1 = cv2.cvtColor(face_1,cv2.COLOR_BGR2GRAY)
  face_1 = cv2.resize(face_1,(24,24))
  face_1 = face_1/255
  face_1 = face_1.reshape(24,24,-1)
  face_1 = np.expand_dims(face_1,axis=0)
  face_predict = model.predict_classes(face_1)
  if(face_predict==0):
    color = (0, 0, 255)
           
    cv2.putText(frame,"No Mask",(x,y-4), font, 1,color,1,cv2.LINE_AA)
    cv2.rectangle(frame, (x,y) , (x+w , y+h) , color , 2)
    # cv2.putText(frame,"No Mask",(0,20), font, 1,color,1,cv2.LINE_AA)
    # cv2.rectangle(frame, (0,0) , (0+width , 0+height) , color , 2)
  else:
    color = (0, 255, 0)
    cv2.putText(frame,"Mask",(x,y-4), font, 1,color,1,cv2.LINE_AA)
    cv2.rectangle(frame, (x,y) , (x+w , y+h) , color , 2)
    # cv2.putText(frame,"Mask",(0,20), font, 1,color,1,cv2.LINE_AA)
    # cv2.rectangle(frame, (0,0) , (0+width , 0+height) , color , 2)
         #break
         

cv2_imshow(frame)
cv2.imwrite('pic1.jpg' ,frame)
if cv2.waitKey(0) & 0xFF == ord('q'):    ### for webcam
        break
cap.release()
cv2.destroyAllWindows()

model.summary()

"""Image Capture(COLAB) """

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript(
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    )
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image
try:
  filename = take_photo()
  print('Saved to {}'.format(filename))
  
  # Show the image which was just taken.
  display(Image(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))

  
!pip3 install mtcnn
from mtcnn.mtcnn import MTCNN   # face detection using MTCNN


filename = "photo.jpg"
img = cv2.imread(filename)
detector = MTCNN()
detector.detect_faces(img)

