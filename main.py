#!/usr/bin/env python
# coding: utf-8

# In[23]:


##### Importing libraries
import cv2
import os
from matplotlib import pyplot as plt
import numpy as np
import glob

##### Part A) Extracting key frames through adaptive threshold 

VEDIO_FILE_NAME = 's09.avi' ## GIve vedio name here

##### Taking Input
cap = cv2.VideoCapture(VEDIO_FILE_NAME)
frame_list = []
cframe = 0
while(True):
    ret, frame= cap.read()
    if not ret:
        break
    name = './data/' + str(cframe) + '.jpg'
    print("creating" +name)
    cv2.imwrite(name,frame)
    frame_list.append(frame)
    cframe += 1

images = {}
index = {}

for imagePath in glob.glob('./data/*.jpg'):
    filename = imagePath[imagePath.rfind("/") + 1:]
                  
    image = cv2.imread(imagePath,1)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    hist = cv2.calcHist([image],[0,1,2],None,[8,8,8],[0,256,0,256,0,256])
    hist = cv2.normalize(hist,None).flatten()
    index[filename] = hist
    
OPENCV_METHODS = ((cv2.HISTCMP_CORREL ),(cv2.HISTCMP_CHISQR),(cv2.HISTCMP_INTERSECT), (cv2.HISTCMP_BHATTACHARYYA))

for method in OPENCV_METHODS:
    results = {}
    reverse = False
    if method in (cv2.HISTCMP_CORREL, cv2.HISTCMP_INTERSECT ):
        reverse = True

for (k, hist) in index.items():
    d = cv2.compareHist(index[k], hist, cv2.HISTCMP_INTERSECT)
    results[k] = d
    print(d)
    
for (k,hist) in index.items():
    mean__ = np.mean(index[k], dtype=np.float64)

    
for (k,hist) in index.items():
    variance = np.var(index[k], dtype=np.float64)
        

print("Variance", variance)
        
standard_deviation = np.sqrt(variance) ### calculating standard deviation
th = mean__ + standard_deviation + 3
print("Threshold value", th)

try:
    if not os.path.exists('keyframes'):
        os.makedirs('keyframes')
except OSError:
    print("Error cant make directories")


cframe1=0
cap = cv2.VideoCapture(VEDIO_FILE_NAME)
for (k,hist) in index.items():
    d = cv2.compareHist(index[k], hist, cv2.HISTCMP_INTERSECT)
    ret, keyframe = cap.read()
    if not ret:
        break
    
    if (d > th):
        name = './keyframes/' + str(cframe1) + '.jpg'
        print("creating" +name)
        cv2.imwrite(name, keyframe )
        cframe1+=1

###### Part B Generating 30fps vedio of key frames

img_array = []
for filename in glob.glob('keyframes/*.jpg'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


# In[ ]:




