# -*- coding: utf-8 -*-
"""face_mask_detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w9nRovvFMSAo2y2-2pQdeW_u6s_U27sr
"""

!pip install kaggle

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d omkargurav/face-mask-dataset

from zipfile import ZipFile
dataset = '/content/face-mask-dataset.zip'

with ZipFile(dataset,'r') as zip:
  zip.extractall()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg
import cv2
from google.colab.patches import cv2_imshow
from PIL import Image

with_mask_list = os.listdir('/content/data/with_mask')
without_mask_list = os.listdir('/content/data/without_mask')

print("length of file containg with mask element ",len(with_mask_list))
print("length of file containing without mask element ",len(without_mask_list))

"""**CREATING LABELS**"""

with_mask_labels = [1]*3725
without_mask_labels = [0]*3828

labels = with_mask_labels + without_mask_labels

"""**DISPLAYING THE IMAGE**"""

with_mask_list[0:5]

without_mask_list[0:5]

# displaying with mask image

img = mpimg.imread('/content/data/with_mask/with_mask_1397.jpg')
implot = plt.imshow(img)
plt.show()

# displaying without mask image

img = mpimg.imread('/content/data/without_mask/without_mask_179.jpg')
implot = plt.imshow(img)
plt.show()

"""**IMAGE PROCESSING**"""

with_mask_path = '/content/data/with_mask/'

data = []

for i in with_mask_list:

  img = Image.open(with_mask_path + i)
  img = img.resize((128,128))
  img = img.convert('RGB')
  img = np.array(img)
  data.append(img)


without_mask_path = '/content/data/without_mask/'

for j in without_mask_list:

  img = Image.open(without_mask_path + j)
  img = img.resize((128,128))
  img = img.convert('RGB')
  img = np.array(img)
  data.append(img)

type(data)

type(data[0])

data[0].shape

x = np.array(data)
y = np.array(labels)

x.shape

y.shape

type(x)

type(y)

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state = 42)

x_train.shape

y_train.shape

# scaling the data

x_train_scaled = x_train/255

x_test_scaled = x_test/255

x_train[0]

x_train_scaled[0]

"""**BUILDING NEURAL NETWORK**"""

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Convolution2D,MaxPooling2D,Flatten,Dense,Conv2D,Dropout

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),activation = 'relu',input_shape = (128,128,3)))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,kernel_size=(3,3),activation = 'relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.5))


model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))

model.add(Dense(2,activation = 'sigmoid'))

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['acc'])

history = model.fit(x_train_scaled,y_train,validation_split=0.1,epochs=10)

"""**MODEL EVALUATION**"""

loss,acc = model.evaluate(x_test_scaled,y_test)

print("accuracy of model is ",round(acc*100,2),"%")

# plotting graph for loss

plt.plot(history.history['loss'],label = "train loss")
plt.plot(history.history['val_loss'],label = "val_loss")
plt.legend()
plt.show()

# plotting graph for accuracy

plt.plot(history.history['acc'],label = "train_acc")
plt.plot(history.history['val_acc'],label = "val_acc")
plt.legend()
plt.show()

"""**PREDECTIVE SYSTEM**"""

input_image_path = input("Enter the path of image : ")

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (128,128))

input_image_scaled = input_image_resize/255

input_image_reshape = np.reshape(input_image_scaled,(1,128,128,3))

input_prediction = model.predict(input_image_reshape)

print(input_prediction)

ans = np.argmax(input_prediction)

if ans == 1:
  print("PERSON IS WEARING MARKS")
else:
  print("PERSON IS NOT WEARING MARKS")

input_image_path = input("Enter the path of image : ")

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (128,128))

input_image_scaled = input_image_resize/255

input_image_reshape = np.reshape(input_image_scaled,(1,128,128,3))

input_prediction = model.predict(input_image_reshape)

print(input_prediction)

ans = np.argmax(input_prediction)

if ans == 1:
  print("PERSON IS WEARING MARKS")
else:
  print("PERSON IS NOT WEARING MARKS")





