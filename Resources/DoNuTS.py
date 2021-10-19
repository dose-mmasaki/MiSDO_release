#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DoNuTS

ルール:
    print 表示するときは英語で。
    ユーザーに表示させる必要のあるエラーメッセージを表示する時はmessagebox, 日本語で。
    その他のエラーメッセージはloggerファイルへ。
    
    
    Docstring を利用すること。
        入力、出力のデータ型は可能な限り記載。
        
    

"""
import argparse
import datetime
import gc
import json
import logging
import os
import pprint
import random
import sqlite3
import sys
import time
import tkinter as tk
from tkinter import messagebox

import pandas as pd
import pydicom
# from memory_profiler import profile
from tqdm.std import tqdm

import DataBase
import donuts_datasets
import funcs

sys.path.append("./")


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
def main(MODALITY, logger, runtime):
    
    pprint.pprint("  ###        ##    #       #######   ###  ")
    pprint.pprint(" #   #       # #   #          #     #   # ")
    pprint.pprint(" #    #      #  #  #          #      #    ")
    pprint.pprint(" #    #  ##  #   # #  #  #    #       #   ")
    pprint.pprint(" #   #  #  # #    ##  #  #    #    #   #  ")
    pprint.pprint("  ###    ##  #     #  ###     #     ###   ")
    
    print("\nStart DoNuTS\n")

    # desktop_dir = os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH') + '/Desktop'
    desktop_dir = os.path.expanduser("~") + '/Desktop'
    # ディレクトリの選択
    dicom_directory = funcs.select_directory(desktop_dir)

    # pathを取得するジェネレータを作成, tqdmのためのtotal_file_cntを取得.
    path_generator, total_file_cnt = funcs.get_path(dicom_directory)
    
    if total_file_cnt==0:
        messagebox.showerror('エラー', 'DICOMファイルが見つかりませんでした。\nプログラムを終了します。')
        sys.exit(0)
    
    else:
        print("Found {} DICOM files.\n".format(total_file_cnt))

    # 実行時間計測の開始
    start = time.time()

    # データベースを呼び出す。
    DATABASE_ALL = DataBase.WriteDB(MODALITY="ALL_DATA", is_dev=False)

    # データの, 新規/重複の数をカウントする
    new_data_cnt = 0
    duplicate_data_cnt = 0

    # ファイルを一つずつ読み込み、処理を開始する。
    # RDSRのみ処理を行う。
    print("Process for RDSR...\n")
    with tqdm(path_generator, total=total_file_cnt) as pbar:
        for i, dicom_path in enumerate(pbar):

            try:
                # DICOMとして読み取る
                dicom_file = pydicom.dcmread(dicom_path)

                _modality = funcs.identify_modality(dicom_file)

                # RDSRファイルを処理
                if _modality in ["XA", "CT"]:
                    # events = funcs.get_IrradiationEvents(dicom_file, MODALITY=_modality)

                    # 照射情報である、Acquisitionを取得する。
                    acquisition_set = funcs.separate_Acquisition(
                        dicom_file, MODALITY=_modality)

                    # 各商社情報からデータを取得する
                    for j, each_acquisition in enumerate(acquisition_set):

                        # temp_dictにデータを格納していく。
                        temp_dict = donuts_datasets.return_json_temprate(
                            MODALITY="Auto")

                        # CTの照射情報を取得
                        if _modality == "CT":
                            try:
                                temp_dict = funcs.extract_data_from_CT_Acquisition(
                                    temp_dict, each_acquisition)
                                CTDoseLengthProductTotal = funcs.extract_CT_Dose_Length_Product_Total(
                                    rdsr_file=dicom_file)
                                temp_dict['CTDoseLengthProductTotal'] = CTDoseLengthProductTotal
                            except:
                                # 不明のエラーの可能性
                                # エラーをlog.txtに書き込む
                                logger.exception(sys.exc_info())
                                pass

                        # XAの照射情報を取得
                        elif _modality == "XA":
                            try:
                                temp_dict = funcs.extract_data_from_angio_Acquisition(
                                    temp_dict, each_acquisition)
                            except:
                                # 不明のエラーの可能性
                                # エラーをlog.txtに書き込む
                                logger.exception(sys.exc_info())
                                pass

                        # ヘッダー情報を書き込む
                        temp_dict = funcs.writeHeader(
                            dicom_file, temp_dict, _modality, dicom_path)

                        temp_dict['PRIMARY KEY'] = temp_dict['SOPInstanceUID'] + \
                            '_' + str(j)
                        temp_dict['Runtime'] = runtime

                        # PRIMARY_KEY が重複するとエラーとなるため、tryで処理する
                        # PRIMARY_KEY 以外のエラーの場合、エラーログを出力
                        try:
                            write_list = [v for v in temp_dict.values()]
                            # Write DB
                            DATABASE_ALL.main(data=write_list)
                            # 新規データのカウント
                            new_data_cnt += 1

                        except Exception as e:
                            # PRIMARY_KEYエラーの時は無視。
                            if "PRIMARY_KEY" in e.args[0]:
                                # 重複データとしてカウント
                                duplicate_data_cnt += 1
                                pass
                            else:
                                # その他のエラーの時はログ出力
                                # エラーをlog.txtに書き込む
                                logger.exception(sys.exc_info())

                # RDSRファイル以外のとき
                else:
                    pass

            except:
                # 不明のエラーの可能性
                logger.exception(sys.exc_info())  # エラーをlog.txtに書き込む
                pass

    # PT, NMが含まれている時、投与量を取得する必要がある。
    # 処理を完了したRDSRファイルに対して、追加処理を行う。
    if MODALITY in ['PT', 'NM', 'Auto']:
        # ジェネレータを再度作成.
        path_generator, total_file_cnt = funcs.get_path(dicom_directory)
        print("Process for Extract Radionuclide Total Dose ... \n")

        with tqdm(path_generator, total=total_file_cnt) as pbar:
            for dicom_path in pbar:
                try:
                    # DICOMとして読み取る
                    dicom_file = pydicom.dcmread(dicom_path)

                    # モダリティを判定する。
                    _modality = funcs.identify_modality(dicom_file)

                    # PT,NMのDICOMファイルに投与量が記載されている。
                    if _modality in ["M_PT", "M_NM"]:

                        # RDSR上のPT,NMの情報と, RDSR以外（検査情報）のDICOMファイルを紐づけるために、
                        # StudyInstanceUID　を利用する。
                        s_UID = str(dicom_file.StudyInstanceUID)

                        # StudyInstanceUID　が一致するデータがあれば処理を開始する。
                        value_list = DATABASE_ALL.query(
                            column="StudyInstanceUID", key=s_UID)

                        # 対応するRDSRファイルが存在しない場合、ヘッダー情報と投与量のみ記載する。
                        if len(value_list) == 0:
                            try:
                                _dose = str(
                                    dicom_file.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose)
                                # temp_dictにデータを格納していく。
                                temp_dict = donuts_datasets.return_json_temprate(
                                    MODALITY="Auto")
                                
                                _modality = _modality[-2:]  # M_XX → XX
                                
                                temp_dict = funcs.writeHeader(
                                    dicom_file, temp_dict, _modality, dicom_path)
                                
                                temp_dict['PRIMARY KEY'] = temp_dict['SOPInstanceUID'] + \
                                    "_" + temp_dict['PatientID']
                                    
                                temp_dict['Runtime'] = runtime
                                
                                temp_dict['RadionuclideTotalDose'] = _dose

                                try:
                                    write_list = [
                                        v for v in temp_dict.values()]
                                    # Write DB
                                    DATABASE_ALL.main(data=write_list)
                                    # 新規データのカウント
                                    new_data_cnt += 1
                                except Exception as e:
                                    # PRIMARY_KEYエラーの時は無視。
                                    if "PRIMARY_KEY" in e.args[0]:
                                        # ここでは重複データとしてカウントしない。
                                        pass
                                    else:
                                        # その他のエラーの時はログ出力
                                        # エラーをlog.txtに書き込む
                                        logger.exception(sys.exc_info())
                            except:
                                # ignore
                                pass

                            pass
                        elif len(value_list) != 0:
                            for value in value_list:
                                # 投与量が記載されていなければ,１レコードずつ書き込む。
                                try:
                                    if value[2] == " ":
                                        _dose = str(
                                            dicom_file.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose)
                                        DATABASE_ALL.update(
                                            id=value[0], modality=_modality[-2:], dose=_dose)
                                except:
                                    # ignore
                                    pass
                except:
                    # ignore
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
    
    
    
    
    # 実行時間計測の終了
    end = time.time()
    print("Processing time : {:.2f} seconds.\n".format(float(end-start)))
    
    print("New {} records, duplicated {} records.\n".format(new_data_cnt, duplicate_data_cnt))


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
        description="Get kind of modaliry")
    parser.add_argument("--modality", help="type of modaliry")
    args = parser.parse_args()

    MODALITY = args.modality
    MODALITY = "Auto" # FIXME: for dev


    main(MODALITY=MODALITY, logger=lg, runtime=runtime)
    
    print('********************Done DoNuTS********************')

    print("End program in 10 seconds.")