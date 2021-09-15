# -*- coding: utf-8 -*-
from cython_modules import DoNuTS
import time
import json
import pandas as pd
if __name__ == '__main__':

    
    
    result = DoNuTS.main()
    latest_result = []
    for x in result:
        try:
            for y in x:
                latest_result.append(y)
        except :
            latest_result.append(x)

    for modality,res in zip(['CT','PT','NM','XA'],result):
        DoNuTS.writeDB_from_list(modality, res)
        
        
    save_name = './Resources/latest'
    
    file_name_json = save_name + ".json"
    file_name_csv = save_name + ".csv"
    

    # json
    with open(file_name_json, mode='wt', encoding='utf-8') as file:
        json.dump(latest_result, file, ensure_ascii=False, indent=1)

    # csv
    df = pd.read_json(file_name_json)
    df.to_csv(file_name_csv, encoding='utf-8')
    
    print("This program will end in 10 seconds")
    time.sleep(10)