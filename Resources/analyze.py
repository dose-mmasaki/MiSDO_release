import argparse
from matplotlib import pyplot as plt
import sqlite3
# import re
import seaborn as sns
# import pandas as pd
import numpy as np

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
                pass
    else:
        result_list_x = [0]
        result_list_y = [0]
        pass
    return result_list_x, result_list_y

def main(sql:str):
    DB_path = './Resources/DONUTS.db'
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    # data[list] [target, PatientSize, PatientWeight]
    tuple_data = cursor.fetchall()
    data_head = []
    data_body = []
    data_unkown = []
    for i, d in enumerate(tuple_data):
        # d[0] is value of target (CTDIvol or DLP)
        if d[0] == " ":
            pass
        else:
            d = list(d)
            if "(Head)" in d[0]:
                r = d[0].replace("(Head)", "")
                d[0] = float(r)
                data_head.append(d)
            elif "(Body)" in d[0]:
                r = d[0].replace("(Body)", "")
                d[0] = float(r)
                data_body.append(d)
            else:
                d[0] = float(d[0])
                data_unkown.append(d)

    

    _BMI_list_Head, _list_Head = calc_BMI(data_head)
    _BMI_list_Body, _list_Body = calc_BMI(data_body)
    _BMI_list_unknown, _list_unknown = calc_BMI(data_unkown)
    
    
        
        
    target = sql.split(" ")[1].split(",")[0]
    
    # ylabel for plot
    if target == "DLP":
        ylabel = "mGy*cm"
    elif target == "MeanCTDIvol":
        ylabel = "mGy"

    # Plot
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(target)
    
    # Head 
    figure_head = sns.boxplot(ax=axes[0][0], data=_list_Head, color="c", whis=np.inf)
    figure_head = sns.stripplot(ax=axes[0][0], data=_list_Head, color="b")
    figure_head.set_ylabel(ylabel)
    figure_head.set_title("Head")
    
    # Head BMI
    figure_head_bmi = sns.scatterplot(ax=axes[1][0], x=_BMI_list_Head, y=_list_Head)
    figure_head_bmi.set_ylabel(ylabel)
    figure_head_bmi.set_xlabel("BMI")
    
    # Body 
    figure_body = sns.boxplot(ax=axes[0][1], data=_list_Body, color="c", whis=np.inf)
    figure_body = sns.stripplot(ax=axes[0][1], data=_list_Body, color="b")
    figure_body.set_ylabel(ylabel)
    figure_body.set_title("Body")
    
    # Body BMI
    figure_body_bmi = sns.scatterplot(ax=axes[1][1], x=_BMI_list_Body, y=_list_Body)
    figure_body_bmi.set_ylabel(ylabel)
    figure_body_bmi.set_xlabel("BMI")
    
    # Unknown 
    figure_unknown = sns.boxplot(ax=axes[0][2], data=_list_unknown, color="c", whis=np.inf)
    figure_unknown = sns.stripplot(ax=axes[0][2], data=_list_unknown, color="b")
    figure_unknown.set_ylabel(ylabel)
    figure_unknown.set_title("Unknown")
    
    # Unknown BMI
    figure_unknown_bmi = sns.scatterplot(ax=axes[1][2], x=_BMI_list_unknown, y=_list_unknown)
    figure_unknown_bmi.set_ylabel(ylabel)
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
    sql = "SELECT MeanCTDIvol,PatientSize,PatientWeight FROM ALL_DATA WHERE Identified_Modality in ('XA','CT') AND WrittenDate LIKE '%1019%'"

    main(sql=sql)
