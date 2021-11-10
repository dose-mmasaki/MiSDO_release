import argparse
import sqlite3
import sys,os

sys.path.append(os.getcwd() + "\\misdo_env\\Lib\\site-packages")

# import pandas as pd
import numpy as np
# import re
import seaborn as sns
from matplotlib import pyplot as plt

import DataBase

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

def main(sql:str):
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
    fig1.suptitle("MeanCTDIvol")
    ylabel1 = "mGy"
    
    # Head 
    figure_head = sns.boxplot(ax=axes1[0][0], data=_ctdi_Head, color="c", whis=np.inf)
    figure_head = sns.stripplot(ax=axes1[0][0], data=_ctdi_Head, color="b")
    figure_head.set_ylabel(ylabel1)
    figure_head.set_title("Head")
    
    # Head BMI
    figure_head_bmi = sns.scatterplot(ax=axes1[1][0], x=_BMI_ctdi_Head, y=_ctdi_Head)
    figure_head_bmi.set_ylabel(ylabel1)
    figure_head_bmi.set_xlabel("BMI")
    
    # Body 
    figure_body = sns.boxplot(ax=axes1[0][1], data=_ctdi_Body, color="c", whis=np.inf)
    figure_body = sns.stripplot(ax=axes1[0][1], data=_ctdi_Body, color="b")
    figure_body.set_ylabel(ylabel1)
    figure_body.set_title("Body")
    
    # Body BMI
    figure_body_bmi = sns.scatterplot(ax=axes1[1][1], x=_BMI_ctdi_Body, y=_ctdi_Body)
    figure_body_bmi.set_ylabel(ylabel1)
    figure_body_bmi.set_xlabel("BMI")
    
    # Unknown 
    figure_unknown = sns.boxplot(ax=axes1[0][2], data=_ctdi_unknown, color="c", whis=np.inf)
    figure_unknown = sns.stripplot(ax=axes1[0][2], data=_ctdi_unknown, color="b")
    figure_unknown.set_ylabel(ylabel1)
    figure_unknown.set_title("Unknown")
    
    # Unknown BMI
    figure_unknown_bmi = sns.scatterplot(ax=axes1[1][2], x=_BMI_ctdi_unknown, y=_ctdi_unknown)
    figure_unknown_bmi.set_ylabel(ylabel1)
    figure_unknown_bmi.set_xlabel("BMI")



    # 
    # DLP
    # 

    # Plot
    fig2, axes2 = plt.subplots(2, 3, figsize=(15, 8))
    fig2.suptitle("DLP")
    ylabel2 = "mGy*cm"
    
    # Head 
    figure_head = sns.boxplot(ax=axes2[0][0], data=_dlp_Head, color="c", whis=np.inf)
    figure_head = sns.stripplot(ax=axes2[0][0], data=_dlp_Head, color="b")
    figure_head.set_ylabel(ylabel2)
    figure_head.set_title("Head")
    
    # Head BMI
    figure_head_bmi = sns.scatterplot(ax=axes2[1][0], x=_BMI_dlp_Head, y=_dlp_Head)
    figure_head_bmi.set_ylabel(ylabel2)
    figure_head_bmi.set_xlabel("BMI")
    
    # Body 
    figure_body = sns.boxplot(ax=axes2[0][1], data=_dlp_Body, color="c", whis=np.inf)
    figure_body = sns.stripplot(ax=axes2[0][1], data=_dlp_Body, color="b")
    figure_body.set_ylabel(ylabel2)
    figure_body.set_title("Body")
    
    # Body BMI
    figure_body_bmi = sns.scatterplot(ax=axes2[1][1], x=_BMI_dlp_Body, y=_dlp_Body)
    figure_body_bmi.set_ylabel(ylabel2)
    figure_body_bmi.set_xlabel("BMI")
    
    # Unknown 
    figure_unknown = sns.boxplot(ax=axes2[0][2], data=_dlp_unknown, color="c", whis=np.inf)
    figure_unknown = sns.stripplot(ax=axes2[0][2], data=_dlp_unknown, color="b")
    figure_unknown.set_ylabel(ylabel2)
    figure_unknown.set_title("Unknown")
    
    # Unknown BMI
    figure_unknown_bmi = sns.scatterplot(ax=axes2[1][2], x=_BMI_dlp_unknown, y=_dlp_unknown)
    figure_unknown_bmi.set_ylabel(ylabel2)
    figure_unknown_bmi.set_xlabel("BMI")

    
    # p2 = sns.boxplot(ax=axes[0][1], data=target_data_all, color="c", whis=np.inf)
    # p2 = sns.stripplot(ax=axes[0][1], data=target_data_all, color="b")
    # p2.set_ylabel(ylabel)
    # p = sns.scatterplot(ax=axes[0][2], x=_BMI_list, y=enable_list)
    # p.set_ylabel(ylabel)

    plt.show()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="show statistics")
    parser.add_argument("--sql", help="sql")
    args = parser.parse_args()

    sql = args.sql
    sql = "SELECT MeanCTDIvol,DLP,PatientSize,PatientWeight FROM ALL_DATA" #FIXME : dev

    main(sql=sql)
