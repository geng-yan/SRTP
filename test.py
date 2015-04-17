# -*- coding:utf-8 -*-


import cv2
import MySQLdb
import numpy as np
from cv2 import imread, imshow
import LSH
import json
import datetime

starttime = datetime.datetime.now()
conn=MySQLdb.connect (
    host='42.121.114.70',
    port=3306,
    user='cccoi',
    passwd='cccoiers',
    db='buildingdetect',
    )
cur=conn.cursor();

result = []
#image = cv.LoadImage("target.jpg", 1)

lsh=LSH.LSH(100,128,table_num=5)
sift=cv2.SIFT()

#insert into database
#have done in 2015/3/26
#for i in range(5,10):
#    print i
#    image1 = cv2.imread(("%d.jpg" % i), 1)
#    h,w,x=image1.shape
#    #have done insert all
#    #cur.execute("insert into image(buildingid,buildingname,filename,height,width) values('%d','build%d','E:\\\%d.jpg','%d','%d');" %(i,i,i,h,w))
#    kp,des=sift.detectAndCompute(image1,None)
#    for j in range(len(des)):
#        x=json.dumps(des[j].tolist())
#        vec = des[j]
#        #cur.execute("insert into keypoint (pictureid,positionx,positiony,size,orient,localdescriptor) values('%d','%f','%f','%f','%f','%s');" % (i,kp[j].pt[0],kp[j].pt[1],kp[j].size,kp[j].angle,x)) 
#        #cur.execute("SELECT LAST_INSERT_ID();")
#        #conn.commit()
#        keypointid=cur.fetchone()[0]
#        #print "done"
#        lsh.index(vec,'%d' % i,keypointid)
#        lsh.index(vec,'%d' % i,0)

#print 'done'
endtime = datetime.datetime.now()
interval=(endtime - starttime).seconds
print "time1",interval
image=cv2.imread('target.png')
rows,cols = image.shape[0],image.shape[1]
M=np.float32(([1,0,100],[0,1,50]))
img=cv2.warpAffine(image,M,(cols,rows))
kp,des=sift.detectAndCompute(image,None)
print len(des)
endtime = datetime.datetime.now()
interval=(endtime - starttime).seconds
print "time2",interval
for vec in des:
    a=lsh.query(vec, 1)
    print "1"
    if a:
        print a[0][0][1],a[0][1]
endtime = datetime.datetime.now()
interval=(endtime - starttime).seconds
print "time1",interval
#conn.commit()
