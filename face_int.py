from flask import Flask
import argparse

import cv2.dnn

from utils import *
import pickle
import os
from os import listdir
import utils
import numpy as np
import pandas as pd
from numpy import asarray
from numpy import expand_dims
from keras_facenet import FaceNet
from PIL import Image as Img
from utils import *


#####################################################################
parser = argparse.ArgumentParser()
MyFaceNet =FaceNet()
parser.add_argument('--model-cfg', type=str, default='./cfg/yolov3-face.cfg',
                    help='path to config file')
parser.add_argument('--model-weights', type=str,
                    default='./model-weights/yolov3-wider_16000.weights',
                    help='path to weights of model')
parser.add_argument('--image', type=str, default='',
                    help='path to image file')
parser.add_argument('--video', type=str, default='',
                    help='path to video file')
parser.add_argument('--src', type=int, default=0,
                    help='source of the camera')
parser.add_argument('--output-dir', type=str, default='outputs/',
                    help='path to the output directory')
args = parser.parse_args()




#
#
# parser = argparse.ArgumentParser()
# MyFaceNet =FaceNet()
# parser.add_argument('--model-cfg', type=str, default='C:/Users/sanjai/KSP face recognition api/cfg',
#                     help='path to config file')
# parser.add_argument('--model-weights', type=str,
#                     default='C:/Users/sanjai/KSP face recognition api/model-weights',
#                     help='path to weights of model')
# parser.add_argument('--image', type=str, default='',
#                     help='path to image file')
# parser.add_argument('--video', type=str, default='',
#                     help='path to video file')
# parser.add_argument('--src', type=int, default=0,
#                     help='source of the camera')
# parser.add_argument('--output-dir', type=str, default='outputs/',
#                     help='path to the output directory')
# args = parser.parse_args()

MyFaceNet =FaceNet()
net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


# folder='C:/Users/sanjai/KSP face recognition api/missing/'
# database={}
# for filename in listdir(folder):
#     path = folder + filename
#     frame = cv2.imread(folder + filename)
#     print(path)
#     # Stop the program if reached end of video
#
#     # Create a 4D blob from a frame.
#     blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
#                                  [0, 0, 0], 1, crop=False)
#
#     # Sets the input to the network
#     net.setInput(blob)
#
#     # Runs the forward pass to get output of the output layers
#     outs = net.forward(get_outputs_names(net))
#
#     # Remove the bounding boxes with low confidence
#     faces = post_process(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
#     print('[i] ==> # detected faces: {}'.format(len(faces)))
#     print('#' * 60)
#
#     # initialize the set of information we'll displaying on the frame
#     info = [
#         ('number of faces detected', '{}'.format(len(faces)))
#
#     ]
#     print(faces)
#     if len(faces) > 0:
#         x1, y1, width, height = faces[0]
#     else:
#         x1, y1, width, height = 1, 1, 10, 10
#
#     print(x1, y1, width, height)
#     x1, y1 = abs(x1), abs(y1)
#     x2, y2 = x1 + width, y1 + height
#
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = Img.fromarray(frame)  # konversi dari OpenCV ke PIL
#     gbr_array = asarray(frame)
#     face = gbr_array[y1:y2, x1:x2]
#
#     face = Img.fromarray(face)
#     face = face.resize((160, 160))
#     face = asarray(face)
#
#     face = expand_dims(face, axis=0)
#     print(face)
#     print(faces)
#     signature = MyFaceNet.embeddings(face)
#     print(signature)
#     database[os.path.splitext(filename)[0]] = signature
#
#
# myfile = open("data.pkl", "wb")
# pickle.dump(database, myfile)
# myfile.close()


myfile = open("data.pkl", "rb")
database = pickle.load(myfile)
myfile.close()

def cosine_similarity(embedding1, embedding2):
    embedding1 = np.squeeze(embedding1)
    embedding2 = np.squeeze(embedding2)
    dot = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return dot / (norm1 * norm2)

def findFaces(data):
    gbr1 = data
    gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
    gbr = Img.fromarray(gbr)  # konversi dari OpenCV ke PIL
    gbr_array = asarray(gbr)

    blob = cv2.dnn.blobFromImage(gbr1, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                 [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(get_outputs_names(net))

    # Remove the bounding boxes with low confidence
    faces = post_process(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
    print(type(faces))
    # index = AnnoyIndex(128, metric='euclidean')
    # for i, signature in enumerate(database.values()):
    #     index.add_item(i, signature)
    # index.build(10)



    for (x1, y1, w, h) in faces:
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + w, y1 + h

        face = gbr_array[y1:y2, x1:x2]

        face = Img.fromarray(face)
        face = face.resize((160, 160))
        face = asarray(face)

        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)



        # _, nearest_indices = index.get_nns_by_vector(signature, 1, include_distances=True)
        # identity = list(database.keys())[nearest_indices[0]]
        # if nearest_indices[0] == len(database):
        #     identity = 'Unknown'
        #     cv2.putText(gbr1, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        #     cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # min_dist =1.0
        # identity = ' '
        # for key, value in database.items():
        #     dist = np.linalg.norm(value - signature)
        #     if dist < min_dist:
        #         min_dist = dist
        #         identity = key
        #
        # print("mindist",min_dist)
        min_similarity = 0.0
        identity = ' '
        for key, value in database.items():
            # print(value.shape)
            # print(signature.shape)
            similarity= cosine_similarity(value,signature)
            # print(similarity)
            if similarity > min_similarity:
                min_similarity = similarity
                identity = key

        if min_similarity>=0.75:
            cv2.putText(gbr1, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
            cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow('camera', gbr1)
            cv2.waitKey(0)
            df = pd.read_excel("Sample Missing Persons FIRS.xlsx")

            # Search for the specific identity
            search_result = df[df["Photo_Full_front"] == identity]

            # Print the rows that contain the identity
            print(search_result)




        else:
            identity = 'Unknown'
            # cv2.putText(gbr1, identity, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
            # cv2.rectangle(gbr1, (x1, y1), (x2, y2), (0, 255, 0), 2)




    # filename = 'photo.jpg'
    # cv2.imwrite(filename, gbr1)

    return gbr1


# def display(image):
#     filename = findFaces(image)
#     img = cv2.imread(filename)
#     cv2.imshow('img', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()



folder1='C:/Users/sanjai/KSP face recognition api/people/'
for filename in listdir(folder1):
    path=folder1 + filename
    print(path)
    frame=cv2.imread(path)
    frame = findFaces(frame)
    # frame = Img.fromarray(frame)
    cv2.imshow("hi",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






# webcam = cv2.VideoCapture(0)
# while True:
#     ret, frame = webcam.read()
#
#     if not ret:
#         print("CAM NOT OPEND")
#         break
#     print(frame)
#
#     frame = findFaces(frame)
#
#     cv2.imshow('camera', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# #



