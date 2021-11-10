import sys
import os
import sqlite3

sys.path.append(os.getcwd() + "\\misdo_env\\Lib\\site-packages")

import pandas as pd
# import tkinter as tk
from tkinter import filedialog
import argparse

"""
SQLを引数にCSVを出力する
"""


def main(SQL):

    DB_path = './Resources/MiSDO.db'
    conn = sqlite3.connect(DB_path)

    df = pd.read_sql_query(SQL, conn)
    conn.close()

    # filename = filedialog.asksaveasfilename()
    filename = filedialog.asksaveasfilename(
        title="名前を付けて保存",
        filetypes=[("csv", ".csv")],  # ファイルフィルタ
        initialdir="./",  # 自分自身のディレクトリ
        defaultextension="csv"
    )
    df.to_csv(filename, header=True, index=None, encoding="shift-jis")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SQLを受け取り，DBからCSVを出力する.")
    parser.add_argument("--sql", help="SELECT文を入力")
    args = parser.parse_args()
    try:
        sql = args.sql
        main(SQL=sql)
    except:
        print("sql が不正です")
