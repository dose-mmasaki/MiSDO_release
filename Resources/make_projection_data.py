#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DCMファイルを読み込み、GUIからトリミング範囲を選択する。
トリミング後、選択範囲のProjection　データが作成され、JSONに保存される。

"""


import argparse
import json
import os
import sys
import time
import tkinter
from tkinter import filedialog, messagebox

import numpy as np
import pyautogui  # 外部ライブラリ
import pydicom
from PIL import Image, ImageChops, ImageTk  # 外部ライブラリ


def cropImage(np_img):
    """Crop

    Args:
        img (ndarray): [description]

    Returns:
        crop_np_img (ndarray): [description]
    """
    img = Image.fromarray(np_img)
    # 画像と同じサイズの空画像を作成
    bg = Image.new("L", img.size, img.getpixel((0, 0)))
    # 差分画像を生成
    diff = ImageChops.difference(img, bg)
    # 背景色との境界を求めて切り抜く. 画像内で値が0でない最小領域を返す
    croprange = diff.convert("L").getbbox()
    crop_img = img.crop(croprange)
    # crop_img.show()
    crop_np_img = np.array(crop_img)

    return crop_np_img

# ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -


def start_point_get(event):
    global global_start_x, global_start_y  # グローバル変数に書き込みを行なうため宣言

    canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除

    # canvas1上に四角形を描画（rectangleは矩形の意味）
    canvas1.create_rectangle(event.x,
                             event.y,
                             event.x + 1,
                             event.y + 1,
                             outline="red",
                             tag="rect1")
    # グローバル変数に座標を格納
    global_start_x, global_start_y = event.x, event.y

# ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -


def rect_drawing(event):

    # ドラッグ中のマウスポインタが領域外に出た時の処理
    if event.x < 0:
        end_x = 0
    else:
        end_x = min(img.width, event.x)
    if event.y < 0:
        end_y = 0
    else:
        end_y = min(img.height, event.y)

    # "rect1"タグの画像を再描画
    canvas1.coords("rect1", global_start_x, global_start_y, end_x, end_y)

# ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - -


def release_action(event):
    # 座標を全てグローバル変数にする
    global global_start_x, global_start_y, global_end_x, global_end_y

    # "rect1"タグの画像の座標を元の縮尺に戻して取得
    global_start_x, global_start_y, global_end_x, global_end_y = [
        int(n) for n in canvas1.coords("rect1")]


def make_projection(np_img, json_path):
    # print(global_start_x, global_start_y, global_end_x, global_end_y)

    np_img = np_img[global_start_y:global_end_y, global_start_x:global_end_x]
    crop_img = cropImage(np_img)

    # Convert 1 >> 0, 255 >> 1
    crop_img = np.where(crop_img == 1, 0, 1)
    # 縦方向にデータを加算する
    np_sum = crop_img.sum(axis=0)
    np_sum_list = list(np_sum)

    str_data = ''
    for l in np_sum_list:
        str_data += str(l)

    # リスト内データをintに変換(Jsonに書き込みできないため)
    # l_i_int = [int(i) for i in np_sum_list]

    proto_txt = text1.get()
    proto_txt = str(proto_txt)

    projection_dict = {proto_txt: str_data}

    # 最終的にdataをjsonに書き込む
    data = []  # 初期化
    # プロトコル名が重複しないようにtmpをupdateする
    tmp = {}  # 初期化
    tmp.update(projection_dict)
    try:
        # 既存データを読み込み
        with open(json_path, mode='r', encoding='utf-8') as jf:
            json_data = json.load(jf)
            for jd in json_data:
                tmp.update(jd)

        # ファイルを削除
        os.remove(json_path)

        # dataに追加
        data.append(tmp)

        # ファイルを作成、書き込み
        with open(json_path, mode='wt', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=4)
    
        messagebox.showinfo("完了", "追加しました。")

    except Exception as e:
        print(e)


# メイン処理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="SELECT DATA_FILE to Add Projection-data")
    parser.add_argument(
        "--projection", help="Projection-data, 'PROTOCOL' or 'SCANNAME'")
    args = parser.parse_args()

    target = args.projection
    

    if target == 'PROTOCOL':
        json_path = "./Resources/PROTOCOL_PROJECTION.json"

    elif target == 'SCANNAME':
        json_path = "./Resources/SCANNAME_PROJECTION.json"

    else:
        print('Incorrect: arg projection.')
        sys.exit()

    try:
        # 処理を行うファイルを選択
        root_select_file = tkinter.Tk()
        root_select_file.attributes("-topmost", True)
        root_select_file.withdraw()
        typ = [('DICOMファイル', '*.DCM')]
        path = filedialog.askopenfilename(title="DICOMファイルを選択", filetypes=typ)
    except Exception as e:
        print(e)
        print("ファイルが選択されませんでした。")
        sys.exit()

    try:
        # read file
        dicom_file = pydicom.read_file(path)
    except Exception as e:
        print(e)
        print("DICOMファイルを読み込めません。")
        sys.exit()

    # uint16 >>> uint8 に変換
    np_img = np.array(dicom_file.pixel_array, dtype='uint8')
    img = Image.fromarray(np_img)

    root = tkinter.Tk()
    root.attributes("-topmost", True)  # tkinterウィンドウを常に最前面に表示

    # tkinterで表示できるように画像変換
    img_tk = ImageTk.PhotoImage(img, master=root)

    # Canvasウィジェットの描画
    canvas1 = tkinter.Canvas(root,
                             bg="black",
                             width=img.width,
                             height=img.height)
    # Canvasウィジェットに取得した画像を描画
    canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

    # Canvasウィジェットを配置し、各種イベントを設定
    canvas1.pack(pady=3)
    canvas1.bind("<ButtonPress-1>", start_point_get)
    canvas1.bind("<Button1-Motion>", rect_drawing)
    canvas1.bind("<ButtonRelease-1>", release_action)

    # プロトコル名を手動入力
    text1 = tkinter.Entry(master=root,
                          width=64)
    text1.pack(pady=3)
    text1.insert(tkinter.END, "プロトコル名を入力")

    # OKボタン
    button1 = tkinter.Button(master=root,
                             text='OK',
                             command=lambda: make_projection(np_img, json_path))
    button1.pack(pady=3)

    # 終了ボタン
    button2 = tkinter.Button(master=root,
                             text='ここをクリックして終了してください',
                             command=lambda: root.quit())
    button2.pack(pady=3)

    root.mainloop()
