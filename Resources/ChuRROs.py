#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ChuRROs

Tesseractを利用する場合,use_tesser = True
Tesseractを利用するとき、prot_lang = 'jpn'or'eng'

ルール:
    print 表示するときは英語で。
    ユーザーに表示させる必要のあるエラーメッセージを表示する時はmessagebox, 日本語で。
    その他のエラーメッセージはloggerファイルへ。
    
    
    Docstring を利用すること。
        入力、出力のデータ型は可能な限り記載。
        
    

"""
import argparse
import datetime
import logging
import glob
import os
import sys
import time
import pprint
import gc
import sqlite3

import pydicom
from tqdm import tqdm
import numpy as np
import pandas as pd
import random
# from memory_profiler import profile

import DataBase
import donuts_datasets
import funcs
import ocr_funcs

ocr_header = {
    'PRIMARY KEY': ' ',
    'WrittenDate': ' ',
    'Runtime': ' ',
    'Path': ' ',
    'Identified Modality': "",
    "SOPInstanceUID": " ",
    "StudyInstanceUID":" ",
    "StudyID": " ",
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
    'Acquisition Protocol': ' '
}

ocr_dict = {
    'CTAcquisitionType': '',
    'TotalMAS': '',
    'ExposureTime': '',
    'MeanCTDIvol': '',
    'DLP': ''
}

def get_logger(logger_name, log_file, f_fmt='%(message)s'):
    """ロガーを取得"""
    # ロガー作成
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # ファイルハンドラ作成
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(f_fmt))

    # ロガーに追加
    logger.addHandler(file_handler)

    return logger

# @profile
def main(prot_lang: str, is_dev, use_tesser, runtime, logger):
    pprint.pprint("   ###  #           ####   ####              ")
    pprint.pprint("  #   # #           #   #  #   #         ### ")
    pprint.pprint(" #      #           ####   ####    ##   #    ")
    pprint.pprint(" #      ####   #  # #  #   #  #   #  #   ##  ")
    pprint.pprint("  #   # #   #  #  # #   #  #   #  #  #     # ")
    pprint.pprint("   ###  #   #  ###  #    # #    #  ##   ###  ")
    print("\nStart ChuRROs\n")
    # 読み取り言語の設定 jpn,eng 以外なら終了
    if prot_lang not in ["jpn", "eng"]:
        print("Incorrect lang")
        sys.exit(0)

    # tesser を使う場合、DefaultProtocolを読み込む
    if use_tesser:
        # debug mode
        if is_dev:
            with open("D:\Donuts\git\src\Resources\DefaultProtocol.txt", "r", encoding='utf-8') as tf:
                defaultlines = tf.read().split("\n")

        else:
            with open("./Resources/DefaultProtocol.txt", "r", encoding='utf-8') as tf:
                defaultlines = tf.read().split("\n")
    else:
        pass

    # デスクトップのディレクトリパスを取得
    desktop_dir = os.path.expanduser("~") + '/Desktop'

    # tk によって選択されたディレクトリ
    dicom_directory = funcs.select_directory(desktop_dir)
    # dicom_directory = "D:/Donuts/Data/secondary_capture_data/secondary_capture_data/001" # FIXME:debug

    # 時間計測スタート
    start = time.time()

    """
    ChuRROｓを実行するために、ユーザーにディレクトリを選択してもらう。
    前提条件として、検査毎にディレクトリが分かれているとする。
    (Ex)
    .DCMは secondary_capture Image
    path/to/data/
                ---001/
                    ---0000001.DCM
                    ---0000002.DCM
                    ---0000003.DCM
                    ---0000004.DCM
                ---002/
                    ---0000001.DCM
                    ---0000002.DCM
                    ---0000003.DCM
                    ---0000004.DCM
    """

    # dicom_directory 内のdir, file を全て取得
    files = os.listdir(dicom_directory)
    # files がディレクトリであった場合、ディレクトリ名を取得。ファイルの場合は何もしない。
    # path/to/data/001,002,003,... >>> 001,002,003
    files_dir = [f for f in files if os.path.isdir(
        os.path.join(dicom_directory, f))]

    # dicom_directoryが最下層のディレクトリの場合、そのディレクトリをfiles_dirとする
    # path/to/data/001 >>> 001
    if len(files_dir) == 0:
        split_last = dicom_directory.split('/')[-1]
        dicom_directory = dicom_directory.replace('/'+split_last, '')
        files_dir.append(split_last)

    del files, desktop_dir,
    gc.collect()

    try:
        del split_last
        gc.collect()
    except:
        # ignore
        pass

    if use_tesser:
        # OCRエンジン
        tool = ocr_funcs.get_tesseract(is_dev)
    else:
        tool = None
        pass

    # DBを初期化 (OCR)
    # DATABASE_OCR = DataBase.WriteDB(MODALITY='OCR', is_dev=is_dev)

    # OCRを実行したDCMデータ数 InstanceNumber=1のデータはカウントに含めない
    data_cnt = 0
    # 新規レコード数
    new_data_cnt = 0
    # 重複レコード数
    duplicate_data_cnt = 0
    # DB のALL_DATA に書き込むためのリスト
    all_data = []

    for folder in tqdm(files_dir, desc='Now OCR Program Running...'):
        # 取得する対象のDCMファイルのパスを取得
        # 以下、path に含まれるDCMのみ読み込む
        path = dicom_directory + "/" + folder + "/**/*.dcm"
        # print(path)
        # データ
        dicom_path = glob.glob(path, recursive=True)
        if len(dicom_path) == 0:
            try:
                path = dicom_directory + "/" + folder + "/*.dcm"
                dicom_path = glob.glob(path)
            except Exception as e:
                print(e)
                print("dicom_pathを取得出来ません。")
                sys.exit()
        else:
            pass

        del path
        gc.collect()

        for d_p in dicom_path:
            dicomfile = pydicom.dcmread(d_p)
            # pixeldataが存在しない場合はエラーになるため，tryで実行する.
            try:
                # InstanceNumber を取得. １なら無視をする。
                # （OCRで読み取りたい情報が存在しないため.(TOSHIBA 製)）
                i_n = str(dicomfile.InstanceNumber)
                pix_np_array = np.array(dicomfile.pixel_array, dtype='uint8')
                
                # 予期せぬ例外を拾う
                try:
                    if i_n == "1":
                        # InsetanceNumberが1のとき、線量情報が存在しないため、passする
                        pass

                    # 1以外の場合、OCRを実行
                    else:
                        data_cnt += 1
                        try:
                            """
                                ひとつ前のDCMファイルで読み取ったプロトコル名を取得する
                                out_list = [{'A':[]},
                                            {'B':[]},
                                            {'C':[]}]
                                            >>> ex_protocol = 'C'
                            """
                            ex_protocol = [k for k in out_list[-1].keys()][0]
                        except:
                            # 前回結果がない場合、Noneとする。
                            ex_protocol = None

                        # out_list: 読み取ったOCRの結果
                        out_list = [] #初期化
                        out_list = ocr_funcs.ocr(np_img=pix_np_array,
                                                prot_lang=prot_lang,
                                                ex_protocol=ex_protocol,
                                                use_tesser=use_tesser,
                                                tool=tool)

                        # DCMファイル毎の結果を格納する。
                        data = []
                        for i, out_dict in enumerate(out_list):
                            prot = [k for k in out_dict.keys()][0]
                            valuelist = out_dict[prot]
                            for j, value in enumerate(valuelist):
                                temp_data_dict = {}

                                # header情報の取得
                                for h_key in ocr_header.keys():
                                    if h_key == 'PRIMARY KEY':

                                        header_info = str(
                                            i) + '_' + str(j) + '_' + dicomfile.SOPInstanceUID
                                        temp_dict = {h_key: header_info}
                                        temp_data_dict.update(temp_dict)

                                    elif h_key == 'WrittenDate':
                                        date = datetime.date.today().strftime('%Y%m%d')

                                        temp_dict = {h_key: date}
                                        temp_data_dict.update(temp_dict)
                                        
                                    elif h_key == "Runtime":
                                        temp_dict = {h_key: runtime}
                                        temp_data_dict.update(temp_dict)

                                    elif h_key == 'Path':
                                        temp_dict = {h_key: d_p}
                                        temp_data_dict.update(temp_dict)

                                    elif h_key == 'Identified Modality':
                                        header_info = dicomfile.Modality
                                        temp_dict = {h_key: header_info}
                                        temp_data_dict.update(temp_dict)

                                    elif h_key == 'Acquisition Protocol':
                                        header_info = prot
                                        temp_dict = {h_key: header_info}
                                        temp_data_dict.update(temp_dict)

                                    else:
                                        try:
                                            header_info = str(
                                                getattr(dicomfile, h_key))
                                            temp_dict = {h_key: header_info}
                                            temp_data_dict.update(temp_dict)
                                        except:
                                            temp_dict = {h_key: ' '}
                                            temp_data_dict.update(temp_dict)

                                for col_i, key in enumerate(ocr_dict.keys()):
                                    try:
                                        temp_dict = {key: value[col_i]}
                                        temp_data_dict.update(temp_dict)
                                    except:
                                        temp_dict = {key: ' '}
                                        temp_data_dict.update(temp_dict)

                                data.append(temp_data_dict)

                        if use_tesser:
                            # プロトコル名をデフォルトの名前に変更
                            for d in data:
                                p = d['Acquisition Protocol']

                                d_protocol = ocr_funcs.calc_Levenshtein(
                                    p, defaultlines)

                                d['Acquisition Protocol'] = d_protocol
                                # all_dataへ追加
                                all_data.append(d)

                        else:
                            for d in data:
                                all_data.append(d)
                            pass

                        # DBへの書き込み
                        # for d in data:
                        #     try:
                        #         write_list = [v for v in d.values()]
                        #         DATABASE_OCR.main(data=write_list)
                        #         new_data_cnt += 1
                        #     except Exception as e:
                        #         # print(e)
                        #         duplicate_data_cnt += 1
                        #         pass
                except :
                    logger.exception(sys.exc_info())
                    
            except:
                # ignore : pixel_arrayが存在しないとき
                pass

            

    # DATABASE_OCR.close()

    print("Writting to DB ...")

    # ALL_DATA table に書き込む
    all_dict = donuts_datasets.return_json_temprate(MODALITY="Auto")
    DATABASE_ALL = DataBase.WriteDB(MODALITY="ALL_DATA", is_dev=is_dev)
    for each_data in all_data:

        # all_dict のvalueを空にする
        all_dict = funcs.clear_dict_value(all_dict)
        try:
            # データをall_dictに書き込み
            each_data = funcs._setdefault(each_data, all_dict)
            all_dict.update(each_data)

            # to DB
            write_list = [v for v in all_dict.values()]
            DATABASE_ALL.main(data=write_list)
            new_data_cnt += 1
        except Exception as e:
            duplicate_data_cnt += 1
            assert "PRIMARY_KEY" in e.args[0], "DB writing Error, {}".format(e)
            pass
    DATABASE_ALL.close()
    
    # CSVに出力するために改めてDBに接続する。
    DB_path = './Resources/DONUTS.db'
    conn = sqlite3.connect(DB_path)
    SQL = "select * from ALL_DATA where Runtime='" + runtime + "'"

    df = pd.read_sql_query(SQL,conn)
    
    save_name = './Resources/latest'
    file_name_json = save_name + ".json"
    file_name_csv = save_name + ".csv"
    
    df.to_csv(file_name_csv, header=True, index=None,encoding="shift-jis")
    

    end = time.time()

    print("Processing time : {:.2f} seconds".format(float(end-start)))
    print("Try {} files.".format(data_cnt))
    print("New {} records, duplicated {} records".format(
        new_data_cnt, duplicate_data_cnt))


if __name__ == '__main__':
    
    date = datetime.date.today()
    date = date.strftime('%Y%m%d')
    random_number = random.randint(0, 1000)
    runtime = date + "_" + str(random_number)
    
    if os.path.isfile('./Resources/log.txt'):
        os.remove('./Resources/log.txt')

    lg = get_logger(__name__, './Resources/log.txt')
    lg.debug('ロギング 開始')
    lg.debug(runtime)
    
    
    parser = argparse.ArgumentParser(
        description="Get language of Protocol. input 'jpn' or 'eng' ")
    parser.add_argument("--lang", help="Language of Protocol.")
    parser.add_argument("--tesser", help="Developer mode? Anser 'yes' or 'no'")
    parser.add_argument("--dev", help="Developer mode? Anser 'yes'")
    args = parser.parse_args()

    prot_lang = args.lang
    tesser = args.tesser
    is_dev = args.dev

    if tesser == 'yes':
        use_tesser = True
    else:
        use_tesser = False

    if is_dev == 'yes':
        is_dev = True
        prot_lang = 'jpn'
    else:
        is_dev = False

    # FIXME:debug
    is_dev = 'yes'
    prot_lang = 'jpn'
    use_tesser = False

    main(prot_lang=prot_lang, is_dev=is_dev, use_tesser=use_tesser, runtime=runtime, logger=lg)

    print("End program in 10 seconds.")
    time.sleep(10)
