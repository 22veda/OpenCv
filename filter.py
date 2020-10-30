import cv2
import os
from imutils import paths
import numpy as np
from Detection import Detection#import your detection model
import shutil

def max_box(bbox):
    max_box = 0
    max_area = 0
    for i,box in enumerate(bbox):
        box = box.astype('int32')
        box_w = box[3] - box[1]
        box_h = box[2] - box[0]
        box_a = box_w*box_h
        if box_a > max_area :
            max_area = box_a
            max_box = i
    return bbox[max_box]

dec = Detection("../models/Detection_mtcnn.pb")#path of your detection model
actor = input()#Name of the person's folder you want to filter
base_path = "PATH_OF_THE_BASE_IMAGE"
base_img = cv2.imread(list(paths.list_images(base_path))[0])
# print(list(paths.list_images(base_path)))
search_path = ["SEARCH_PATH"]

filtered_move = []
deleted_move = []
# ve.append(lis)


base_img = cv2.resize(base_img,(400,400))
for k,search in enumerate(search_path):
    search_paths = list(paths.list_images(search))
    l = len(search_paths)
    j = 0
    left = 0
    count = 0
    while(j<l):

    #for j in range(len(search_paths)):
        
        if left == 0:
            if k == 0: 
                deleted_move.append([0])
            else:
                filtered_move.append([0])
        else:
            left = left-1
        i = search_paths[j]
        print(i)
        first = i.split("/")[-2]#split only if you have more folders inside the main folder
        second = i.split("/")[-1]#split only if you have more folders inside the main folder
        img = cv2.imread(i)
        try:
            img = cv2.resize(img,(400,400))
            bbox, scores, pts = dec.detect(img)
            if len(bbox) == 0:
                if k == 1:
                    filtered_move[j] = [1,i,str(search_path[k-1]+"/"+first+"/"+second)]
                j += 1
                continue
            if len(bbox) > 1: bbox = [max_box(bbox)]
            box = bbox[0]
            box = box.astype('int32')
            face = img[box[0]:box[2] , box[1]:box[3]]
            if face.shape[0]!=0 and face.shape[1]!=0:
                face = cv2.resize(face,(400,400))
                img2 = np.concatenate((base_img,img,face),axis=1)
            else:
                print(box)
                img2 = np.concatenate((base_img,img),axis = 1)
            cv2.imshow("channel",img2)
            key = cv2.waitKey()
            
            if key == ord('l'):
                j = j-2
                left = left+2
            elif key == ord('y'):
                if k == 0:
                    deleted_move[j] = [1,i,str(search_path[k+1]+"/"+first+"/"+second)]
                else:
                    filtered_move[j] = [0]
            elif key == ord('n'):
                if k == 1:
                    filtered_move[j] = [1,i,str(search_path[k-1]+"/"+first+"/"+second)]

                else:
                    deleted_move[j] = [0]
            
        except Exception as e:
            print('Invalid frame',e)
            cv2.imshow("chann",img)
            key = cv2.waitKey()
            if key == ord('c'):
                pass
        j += 1
        # print(deleted_move[:20])
        # print(filtered_move[:20])
for x1 in range(len(filtered_move)):
    if filtered_move[x1][0] == 1:
        src = filtered_move[x1][1]
        dest = filtered_move[x1][2]
        shutil.move(src,dest)#moves all the mismatched images to the destination folder
for x2 in range(len(deleted_move)):
    if deleted_move[x2][0] == 1:
        src = deleted_move[x2][1]
        dest = deleted_move[x2][2]
        shutil.move(src,dest)#moves all the valid images to the filtered folder
