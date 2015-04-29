# -*- coding:utf-8 -*-


import cv2
import numpy as np
from cv2 import imread, imshow
import LSH

result = []
#image = cv.LoadImage("target.jpg", 1)

lsh=LSH.LSH(100,128,table_num=5)
kp=[[] for i in range(155)]
sift=cv2.SIFT(2000)
for i in range(1, 155):
    print i
    image1 = cv2.imread(("/Users/mcdreamy/Documents/test2/%d.jpg" % i), 1)
    x=0
    image1=cv2.resize(image1,(0,0),fx=0.4,fy=0.4)
    tkp,des=sift.detectAndCompute(image1,None)
    print len(tkp)
    kp[i-1].append(tkp)
    for vec in des:
        #print vec
        lsh.index(vec,i*100000+x)
        x=x+1
while 1:
    file_name=raw_input("please input the file name");
    image=cv2.imread(file_name)

    tkp,des=sift.detectAndCompute(image,None)
    x=0
    count=[0]*155
    former = [[] for i in range(155)];
    latter = [[] for i in range(155)]
    for vec in des:
        a=lsh.query(vec, 1)
        if a:
            ind = a[0][0][1];
            img_no=ind/100000;kp_no=ind%100000;
        #print img_no,kp_no,len(kp[img_no-1])
       # print kp[img_no-1]
            count[img_no-1]=count[img_no-1]+1
            former[img_no-1].append(tkp[x].pt)# former数组存储的是query图中关键点的坐标
            latter[img_no-1].append(kp[img_no-1][0][kp_no-1].pt)#latter存储的是数据库里面的图的关键点的坐标（index与former数据里面一一对应）
        x=x+1
        #print count


    for i in range(155):
        if count[i]>3:
            H,m = cv2.findHomography(np.float32(former[i]).reshape(-1,1,2),np.float32(latter[i]).reshape(-1,1,2),cv2.RANSAC);
    i=count.index(max(count))
    H,m = cv2.findHomography(np.float32(former[i]).reshape(-1,1,2),np.float32(latter[i]).reshape(-1,1,2),cv2.RANSAC);
    print i,m
    