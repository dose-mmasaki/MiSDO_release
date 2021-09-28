import argparse
import datetime
import glob
import os
import sys
import time

import pydicom
from PIL import Image, ImageChops
from tqdm import tqdm

import DataBase
import donuts_datasets
import funcs
import ocr_funcs
 
ocr_header = {
    'PRIMARY KEY':' ',
    'WittenDate' :' ',
    'Path':' ',
    'Identified Modality':"",
    "SOPInstanceUID":" ",
    "StudyID":" ",
    "ManufacturerModelName": " ",
    "PatientID": " ",
    "StudyDate": " ",
    "PatientName": " ",
    "StudyDescription": " ",
    "PatientBirthDate": " ",
    "PatientSex": " ",
    "PatientAge": " ",
    "PatientSize": " ",
    "PatientWeight": " ",
    'AccessionNumber': ' ',
    'Acquisition Protocol':' '
    }

ocr_dict = {
    'CTAcquisitionType':'',
    'TotalMAS':'',
    'ExposureTime':'',
    'MeanCTDIvol':'',
    'DLP':''
    }

def main(prot_lang: str, is_dev):
    if prot_lang not in ["jpn", "eng"]:
        print("Incorrect lang")
        sys.exit(0)
    
    if is_dev:
        with open("D:\Donuts\git\src\Resources\DefaultProtocol.txt","r", encoding='utf-8') as tf:
            defaultlines = tf.read().split("\n")
    
    else:
        with open("./Resources/DefaultProtocol.txt","r", encoding='utf-8') as tf:
            defaultlines = tf.read().split("\n")
    
    
    
    desktop_dir = os.path.expanduser("~") + '/Desktop'

    dicom_directory = funcs.select_directory(desktop_dir)
    
    start = time.time()
    
    files = os.listdir(dicom_directory)
    files_dir = [f for f in files if os.path.isdir(os.path.join(dicom_directory, f))]
    
    table = 'OCR'
    DATABASE = DataBase.WriteDB(MODALITY=table, is_dev=is_dev)
    
    # OCRエンジン
    tool = ocr_funcs.get_tesseract(is_dev)
    
    if len(files_dir) == 0:
        split_last = dicom_directory.split('/')[-1]
        dicom_directory = dicom_directory.replace('/'+split_last,'')
        files_dir.append(split_last)
    
    data_cnt = 0
    new_data_cnt = 0
    duplicate_data_cnt = 0
    all_data = []
    for folder in tqdm(files_dir, desc='Now OCR Program Running...') :
        path = dicom_directory + "/" + folder + "/**/*.dcm"
        # print(path)
        #データ
        dicom_path = glob.glob(path,recursive=True)
        if len(dicom_path) == 0:
            try:
                path = dicom_directory + "/" + folder + "/*.dcm"
                dicom_path = glob.glob(path)
            except :
                pass
        # print(dicom_path)
        try:
            dicomfiles = [pydicom.dcmread(p) for p in dicom_path]
        except :
            dicomfiles = []
            pass
    
        for f,path in zip(dicomfiles,dicom_path):
                # pixeldataが存在しない場合はエラーになるため，escapeする
            try:
                i_n = str(f.InstanceNumber)
                if i_n != "1":
                    data_cnt += 1
                    try:
                        ex_protocol = list(out_dict)[-1]
                    except:
                        ex_protocol = None

                    out_dict, header_index = ocr_funcs.ocr(dicomfile=f,
                                                tool=tool,
                                                prot_lang=prot_lang,
                                                ex_protocol=ex_protocol)
                    # out_dict = ocr_funcs.replace_and_split(out_dict=out_dict)
                    
                    
                    data = []
                    for i,prot in enumerate(out_dict.keys()):
                        valuelist = out_dict[prot]
                        for j,value in enumerate(valuelist):
                            temp_data_dict = {}
                            
                            # header情報の取得
                            for h_key in ocr_header.keys():
                                if h_key == 'PRIMARY KEY':
                                    
                                    header_info = str(i) + '_' + str(j) + '_' + f.SOPInstanceUID
                                    temp_dict = {h_key:header_info}
                                    temp_data_dict.update(temp_dict)
                                    
                                elif h_key == 'WittenDate':
                                    date = datetime.date.today().strftime('%Y%m%d')
                                    
                                    temp_dict = {h_key:date}
                                    temp_data_dict.update(temp_dict)
                                    
                                elif h_key == 'Path':
                                    temp_dict = {h_key:path}
                                    temp_data_dict.update(temp_dict)
                                    
                                elif h_key == 'Identified Modality':
                                    header_info = f.Modality
                                    temp_dict = {h_key:header_info}
                                    temp_data_dict.update(temp_dict)
                                    
                                elif h_key == 'Acquisition Protocol':
                                    header_info = prot
                                    temp_dict = {h_key:header_info}
                                    temp_data_dict.update(temp_dict)
                                
                                else:
                                    try:
                                        header_info = str(getattr(f, h_key))
                                        temp_dict = {h_key:header_info}
                                        temp_data_dict.update(temp_dict)
                                    except:
                                        temp_dict = {h_key:' '}
                                        temp_data_dict.update(temp_dict)
                            
                            
                            for col_i,key in enumerate(ocr_dict.keys()):
                                try:
                                    temp_dict = {key:value[col_i]}
                                    temp_data_dict.update(temp_dict)
                                except:
                                    temp_dict = {key:' '}
                                    temp_data_dict.update(temp_dict)
                                
                            
                            data.append(temp_data_dict)
                            
                    
                    # プロトコル名をデフォルトの名前に変更
                    for d in data:
                        p = d['Acquisition Protocol']
                        
                        d_protocol = ocr_funcs.calc_Levenshtein(p, defaultlines)
                        
                        d['Acquisition Protocol'] = d_protocol
                        #all_dataへ追加
                        all_data.append(d)
                        
                    
                    # DBへの書き込み
                    for d in data:
                        try:
                            write_list = [v for v in d.values()]
                            DATABASE.main(data=write_list)
                            new_data_cnt += 1
                        except Exception as e:
                            # print(e)
                            duplicate_data_cnt += 1
                            pass
            except Exception as e:
                print(e)
                
    DATABASE.close()
    
    # ALL_DATA table に書き込む
    all_dict = donuts_datasets.return_json_temprate(MODALITY="Auto")
    DATABASE = DataBase.WriteDB(MODALITY="ALL_DATA", is_dev=is_dev)
    for each_data in all_data:
        
        # all_dict のvalueを空にする
        all_dict = funcs.clear_dict_value(all_dict)
        try:
            # データをall_dictに書き込み
            each_data = funcs._setdefault(each_data, all_dict)
            all_dict.update(each_data)
            
            # to DB
            write_list = [v for v in all_dict.values()]
            DATABASE.main(data=write_list)
        except Exception as e:
            assert "PRIMARY_KEY" in  e.args[0], "DB writing Error, {}".format(e)
            pass
    DATABASE.close()
    
    end = time.time()
    
    print("Processing time : {} seconds".format(int(end-start)))
    print("New {} records, duplicated {} records".format(new_data_cnt, duplicate_data_cnt))
    print("OCR done {} Captured files．".format(data_cnt))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get language of Protocol. input 'jpn' or 'eng' ")
    parser.add_argument("--lang", help="Language of Protocol.")
    parser.add_argument("--dev", help="Developer mode? Anser 'yes'")
    args = parser.parse_args()
    
    prot_lang = args.lang
    is_dev = args.dev
    
    
    if is_dev == 'yes':
        is_dev=True
        prot_lang = 'jpn'
    else:
        is_dev=False
        
        

        
    main(prot_lang=prot_lang, is_dev=is_dev)

    print("End program in 10 seconds.")
    time.sleep(10)
