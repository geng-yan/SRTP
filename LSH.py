'''
Created on Mar 22, 2015

@author: mcdreamy
'''
import cv2
import MySQLdb
import numpy as np
from cv2 import imread, imshow
import json

conn=MySQLdb.connect (
    host='42.121.114.70',
    port=3306,
    user='cccoi',
    passwd='cccoiers',
    db='buildingdetect',
    )
cur=conn.cursor();


class LSH(object):
    '''
    classdocs
    '''


    def __init__(self, hash_bits,input_dim,table_num):
        '''
        Constructor
        '''
        self.hash_bits=hash_bits # the dimension of the space to be projected
        self.input_dim=input_dim # the dimension of the input
        self.table_num=table_num # the number of the para hash tables
        self._init_uniform_planes() # init the project transform matrix
        self._init_storage() 
        
    def _init_storage(self):
        '''
        Use the dict data structure to store the hash key
        '''
        self.hash_tables=[dict() for i in range(self.table_num)]
    def _init_uniform_planes(self):
        '''
        Init the transform matrix
        one for each hash table 
        '''
        #fileHandle = open ( 'matrix.txt', 'w' )
        self.uniform_planes=[self._generate_uniform_planes() for _ in xrange(self.table_num)]
        self.load_matrix()
    
    def _generate_uniform_planes(self):
        '''
        randn is based on the uniform distribution
        '''
        return np.random.randn(self.hash_bits,self.input_dim)
    
    def _hash(self,plane,input_point):
        '''
        Calculate the hash value
        '''
        try:
            input_point=np.array(input_point)
            projection=np.dot(plane,input_point)
        except:
            pass
        return "".join(['1' if i>0 else '0' for i in projection])

    def index(self,input_point,extra_data=None,keypointid=1):
        '''
        Description
        '''
        if isinstance(input_point, np.ndarray):
            input_point=input_point.tolist()
        if extra_data:
            value =(tuple(input_point),extra_data)
        else:
            value=tuple(input_point)
        for i,table in enumerate(self.hash_tables):
            ret=self._hash(self.uniform_planes[i], input_point)
            #table.append(self._hash(self.uniform_planes[i], input_point),value)
            table.setdefault(ret,[]).append(value)
            
            #cur.execute("insert into hashval (keypointid,hashtableid,hashvalue) values ('%d','%d','%s');" %(keypointid,i,ret))
            #conn.commit()
        #print self.hash_tables[0]
                        
    def query(self,query_point,num_results=None):
        '''
        Description
        '''
        if not num_results:
            num_results=1;
        candidates=set()
        for i,table in enumerate(self.hash_tables):
            #print i
            #print 'done2'
            #print table
            hash_value=self._hash(self.uniform_planes[i], query_point)
            #print hash_value
            cur.execute("select kp.localdescriptor, i.buildingid from keypoint kp inner join image i  on kp.imageid=i.imageid where kp.keypointid in ( select keypointid from hashval where hashtableid=%d and hashvalue=Cast('%s' as binary(105)))" % (i,hash_value))
            #conn.commit()
            #[localdescriptors,buildingids]=cur.fetchall()
            #print table.get(hash_value),hash_value
            #print(table.get(hash_value,[]))
            x=cur.fetchall()
            #print type(x)
            #print x
            candidates.update(x)
            #candidates.update([])
            #candidates.update(table.get(hash_value,[]))

        if len(candidates)!=0:
            candidates=[(i,self._distance(query_point,json.loads(i[0]))) for i in candidates]
        #print candidates[:0];
            candidates.sort(key=lambda x:x[1])
            return candidates[:num_results]
        else:
            return 0
        
        
        
    def _distance(self,x,y):
        '''
        Euclidean distance
        '''
        diff=np.array(x)-y
        return np.sqrt(np.dot(diff,diff))

    #def save_matrix(self):
    #    print"in"
    #    print self.table_num
    #    for i in range(self.table_num):
    #        np.save(("%d" % i),self.uniform_planes[i]);
    #    print"done"
            
    def load_matrix(self):
        
        for i in range(self.table_num):
            self.uniform_planes[i]=np.load("%d.npy" % i).tolist();
    def load_hashtable(self):
        cur.execute("select keypointid,hashtableid,hashvalue from hashval");
        for row in cur.fetchall():
                self.hash_tables[row[1]].setdefault(row[2],[]).append(row[0])
                print row[1]
        
        
        
        
        
        
