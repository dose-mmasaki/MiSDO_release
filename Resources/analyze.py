import argparse
from matplotlib import pyplot as plt
import sqlite3
import re
import seaborn as sns
import pandas as pd
import numpy as np


def main(target: str, modality: str):
    DB_path = './Resources/DONUTS.db'
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()
    sql = "SELECT " + target + ", PatientSize, PatientWeight \
        FROM ALL_DATA \
            WHERE Identified_Modality in " + modality
    cursor.execute(sql)
    # data[list] [target, PatientSize, PatientWeight]
    tuple_data = cursor.fetchall()
    data_head = []
    data_body = []
    data_unkown = []
    for i, d in enumerate(tuple_data):
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

    CTDIvol_head = [x[0] for x in data_head]
    CTDIvol_body = [x[0] for x in data_body]
    data_all = []
    data_all = data_all + data_head
    data_all = data_all + data_body
    data_all = data_all + data_unkown

    target_data_all = [x[0] for x in data_all]

    _BMI_list = []
    enable_list = []
    for data in data_all:
        if data[1] != " " and data[2] != " ":
            _BMI = float(data[2])/(float(data[1])**2)
            _BMI_list.append(_BMI)
            enable_list.append(data[0])
        else:
            pass

    # ylabel for plot
    if target == "DLP":
        ylabel = "mGy*cm"
    elif target == "MeanCTDIvol":
        ylabel = "mGy"

    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    fig.suptitle(target)
    p1 = sns.boxplot(ax=axes[0], data=target_data_all, color="c", whis=np.inf)
    p1 = sns.stripplot(ax=axes[0], data=target_data_all, color="b")
    p1.set_ylabel(ylabel)
    p = sns.scatterplot(ax=axes[1], x=_BMI_list, y=enable_list)
    p.set_ylabel(ylabel)

    plt.show()

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="show statistics")
    parser.add_argument("--target", help="CTDIvol or DLP")
    parser.add_argument("--modality", help="modality   ex) '('CT', 'PT')' ")
    args = parser.parse_args()

    target = args.target
    modality = args.modality

    main(target=target, modality=modality)
