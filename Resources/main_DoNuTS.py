# -*- coding: utf-8 -*-
from cython_modules import DoNuTS
import time
if __name__ == '__main__':

    
    
    result = DoNuTS.main()
    
    for modality,res in zip(['CT','PT','NM','XA'],result):
        DoNuTS.writeDB_from_list(modality, res)
    
    print("This program will end in 10 seconds")
    time.sleep(10)