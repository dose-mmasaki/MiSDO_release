import argparse
import sqlite3
import sys,os
import logging

sys.path.append(os.getcwd() + "\\misdo_env\\Lib\\site-packages")

# import pandas as pd
import numpy as np
# import re
import seaborn as sns
from matplotlib import pyplot as plt

import DataBase

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

def calc_BMI(x : list):
    if len(x)!=0:
        result_list_x = []
        result_list_y = []
        for data in x:
            if data[1] != " " and data[2] != " ":
                _BMI = float(data[2])/(float(data[1])**2)
                result_list_x.append(_BMI)
                result_list_y.append(data[0])
            else:
                result_list_x.append(0)
                result_list_y.append(data[0])
                pass
    else:
        result_list_x = [0]
        result_list_y = [0]
        pass
    return result_list_x, result_list_y

def return_needs_from_list(target_list:list, list_of_index:list)->list:
    temp = []
    for i in list_of_index:
        temp.append(target_list[i])
    return temp

def main(sql:str, logger):
    try:
        DATABASE_ALL = DataBase.DB("ALL_DATA", is_dev=False)
        tuple_data = DATABASE_ALL.fetchall(sql)

        ctdi_head = []
        ctdi_body = []
        ctdi_unkown = []
        dlp_head = []
        dlp_body = []
        dlp_unkown = []
        for i, d in enumerate(tuple_data):
            # d[0] is value of target CTDIvol
            if d[0] == " ":
                pass
            else:
                d = list(d)
                if "(Head)" in d[0]:
                    r = d[0].replace("(Head)", "")
                    d[0] = float(r)
                    ctdi_head.append(return_needs_from_list(d,[0,2,3]))
                elif "(Body)" in d[0]:
                    r = d[0].replace("(Body)", "")
                    d[0] = float(r)
                    ctdi_body.append(return_needs_from_list(d,[0,2,3]))
                else:
                    d[0] = float(d[0])
                    ctdi_unkown.append(return_needs_from_list(d,[0,2,3]))
            
            # d[1] is value of target DLP
            if d[1] == " ":
                pass
            else:
                d = list(d)
                if "(Head)" in d[1]:
                    r = d[1].replace("(Head)", "")
                    d[1] = float(r)
                    dlp_head.append(return_needs_from_list(d,[1,2,3]))
                elif "(Body)" in d[1]:
                    r = d[1].replace("(Body)", "")
                    d[1] = float(r)
                    dlp_body.append(return_needs_from_list(d,[1,2,3]))
                else:
                    d[1] = float(d[1])
                    dlp_unkown.append(return_needs_from_list(d,[1,2,3]))

        

        _BMI_ctdi_Head, _ctdi_Head = calc_BMI(ctdi_head)
        _BMI_ctdi_Body, _ctdi_Body = calc_BMI(ctdi_body)
        _BMI_ctdi_unknown, _ctdi_unknown = calc_BMI(ctdi_unkown)
        
        _BMI_dlp_Head, _dlp_Head = calc_BMI(dlp_head)
        _BMI_dlp_Body, _dlp_Body = calc_BMI(dlp_body)
        _BMI_dlp_unknown, _dlp_unknown = calc_BMI(dlp_unkown)
        
        
            
            
        # target = sql.split(" ")[1].split(",")[0]
        
        # # ylabel for plot
        # if target == "DLP":
        #     ylabel = "mGy*cm"
        # elif target == "MeanCTDIvol":
        #     ylabel = "mGy"


        # 
        # CTDIvol
        # 

        # Plot
        fig1, axes1 = plt.subplots(2, 3, figsize=(15, 8))
        fig1.suptitle("MeanCTDIvol/DLP")
        ylabel1 = "mGy"
        ylabel2 = "mGy*cm"
        
        # Head 
        figure_ctdi_head = sns.boxplot(ax=axes1[0][0], data=_ctdi_Head, color="c", whis=np.inf)
        figure_ctdi_head = sns.stripplot(ax=axes1[0][0], data=_ctdi_Head, color="b")
        figure_ctdi_head.set_ylabel(ylabel1)
        figure_ctdi_head.set_title("Head")
        
        # Body 
        figure_ctdi_body = sns.boxplot(ax=axes1[0][1], data=_ctdi_Body, color="c", whis=np.inf)
        figure_ctdi_body = sns.stripplot(ax=axes1[0][1], data=_ctdi_Body, color="b")
        figure_ctdi_body.set_ylabel(ylabel1)
        figure_ctdi_body.set_title("Body")
        
        # Unknown 
        figure_ctdi_unknown = sns.boxplot(ax=axes1[0][2], data=_ctdi_unknown, color="c", whis=np.inf)
        figure_ctdi_unknown = sns.stripplot(ax=axes1[0][2], data=_ctdi_unknown, color="b")
        figure_ctdi_unknown.set_ylabel(ylabel1)
        figure_ctdi_unknown.set_title("Unknown")
        
        # Head DLP
        figure_dlp_head = sns.boxplot(ax=axes1[1][0], data=_dlp_Head, color="c", whis=np.inf)
        figure_dlp_head = sns.stripplot(ax=axes1[1][0], data=_dlp_Head, color="b")
        figure_dlp_head.set_ylabel(ylabel2)    
        # Body DLP
        figure_dlp_body = sns.boxplot(ax=axes1[1][1], data=_dlp_Body, color="c", whis=np.inf)
        figure_dlp_body = sns.stripplot(ax=axes1[1][1], data=_dlp_Body, color="b")
        figure_dlp_body.set_ylabel(ylabel2)    
        # Unknown DLP
        figure_dlp_unknown = sns.boxplot(ax=axes1[1][2], data=_dlp_unknown, color="c", whis=np.inf)
        figure_dlp_unknown = sns.stripplot(ax=axes1[1][2], data=_dlp_unknown, color="b")
        figure_dlp_unknown.set_ylabel(ylabel2)


        # 
        # BMI
        # 

        # Plot
        fig2, axes2 = plt.subplots(2, 3, figsize=(15, 8))
        fig2.suptitle("Correlation between MeanCTDIvol/DLP and BMI")
        

        # Head ctdi_BMI
        figure_head_ctdi_bmi = sns.scatterplot(ax=axes2[0][0], x=_BMI_ctdi_Head, y=_ctdi_Head)
        figure_head_ctdi_bmi.set_ylabel(ylabel1)
        figure_head_ctdi_bmi.set_xlabel("CTDI_BMI")
        
        
        # Body ctdi_BMI
        figure_body_ctdi_bmi = sns.scatterplot(ax=axes2[0][1], x=_BMI_ctdi_Body, y=_ctdi_Body)
        figure_body_ctdi_bmi.set_ylabel(ylabel1)
        figure_body_ctdi_bmi.set_xlabel("CTDI_BMI")
        
        
        # Unknown ctdi_BMI
        figure_unknown_ctdi_bmi = sns.scatterplot(ax=axes2[0][2], x=_BMI_ctdi_unknown, y=_ctdi_unknown)
        figure_unknown_ctdi_bmi.set_ylabel(ylabel1)
        figure_unknown_ctdi_bmi.set_xlabel("CTDI_BMI")
        
        # Head dlp_BMI
        figure_head_dlp_bmi = sns.scatterplot(ax=axes2[1][0], x=_BMI_dlp_Head, y=_dlp_Head)
        figure_head_dlp_bmi.set_ylabel(ylabel2)
        figure_head_dlp_bmi.set_xlabel("CTDI_BMI")
        
        
        # Body dlp_BMI
        figure_body_dlp_bmi = sns.scatterplot(ax=axes2[1][1], x=_BMI_dlp_Body, y=_dlp_Body)
        figure_body_dlp_bmi.set_ylabel(ylabel2)
        figure_body_dlp_bmi.set_xlabel("DLP_BMI")
        
        
        # Unknown dlp_BMI
        figure_unknown_dlp_bmi = sns.scatterplot(ax=axes2[1][2], x=_BMI_dlp_unknown, y=_dlp_unknown)
        figure_unknown_dlp_bmi.set_ylabel(ylabel2)
        figure_unknown_dlp_bmi.set_xlabel("DLP_BMI")

        
        # p2 = sns.boxplot(ax=axes[0][1], data=target_data_all, color="c", whis=np.inf)
        # p2 = sns.stripplot(ax=axes[0][1], data=target_data_all, color="b")
        # p2.set_ylabel(ylabel)
        # p = sns.scatterplot(ax=axes[0][2], x=_BMI_list, y=enable_list)
        # p.set_ylabel(ylabel)

        plt.show()
    
    except Exception as e:
        logger.exception(sys.exc_info())
    

if __name__ == '__main__':
    if os.path.isfile('./Resources/log.txt'):
        os.remove('./Resources/log.txt')
    lg = get_logger(__name__, './Resources/log.txt')
    lg.debug('ロギング 開始')
    lg.debug('Analyze')

    parser = argparse.ArgumentParser(description="show statistics")
    parser.add_argument("--sql", help="sql")
    args = parser.parse_args()

    sql = args.sql
    sql = "SELECT MeanCTDIvol,DLP,PatientSize,PatientWeight FROM ALL_DATA" #FIXME : dev

    main(sql=sql, logger=lg)
