'''
Created on Mar 22, 2015

@author: mcdreamy
'''
import MySQLdb
import numpy as np
#conn=MySQLdb.connect(
#    host='127.0.0.1',
#    port='3306',
#    user='root',
#    passwd='',
#    db='srtp',
#)
#cur=conn.cursor();
class LSH(object):
    '''
    classdocs
    '''


    def __init__(self, hash_bits,input_dim,table_num):
        '''
        Constructor
        '''
        self.hash_bits=hash_bits
        self.input_dim=input_dim
        self.table_num=table_num
        self._init_uniform_planes()
        self._init_storage()
        
    def _init_storage(self):
        '''
        Description
        '''
        self.hash_tables=[dict() for i in range(self.table_num)]
    def _init_uniform_planes(self):
        '''
        Description
        '''
        self.uniform_planes=[self._generate_uniform_planes() for _ in xrange(self.table_num)]
        
    def _generate_uniform_planes(self):
        '''
        Description
        '''
        return np.random.randn(self.hash_bits,self.input_dim)
    
    def _hash(self,plane,input_point):
        '''
        Description
        '''
        try:
            input_point=np.array(input_point)
            projection=np.dot(plane,input_point)
        except:
            pass
        return "".join(['1' if i>0 else '0' for i in projection])
    def index(self,input_point,extra_data=None):
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
            #table.append_val(self._hash(self.uniform_planes[i], input_point),value)
            table.setdefault(self._hash(self.uniform_planes[i], input_point),[]).append(value)
        #print self.hash_tables[0]
    def query(self,query_point,num_results=None):
        '''
        Description
        '''
        if not num_results:
            num_results=1;
        candidates=set()
        for i,table in enumerate(self.hash_tables):
            hash_value=self._hash(self.uniform_planes[i], query_point)
            #print table.get(hash_value),hash_value
            #print hash_value
            candidates.update(table.get(hash_value,[]))
        candidates=[(i,self._distance(query_point,i[0])) for i in candidates]
        candidates.sort(key=lambda x:x[1])
        return candidates[:num_results]
        
        
        
        
    def _distance(self,x,y):
        diff=np.array(x)-y
        return np.sqrt(np.dot(diff,diff))
    
            
            
            
    
    
    
        
        
        
        
        