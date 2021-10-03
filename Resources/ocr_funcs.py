import difflib
import glob
import os
import re
import json
import gc

import Levenshtein
import numpy as np
import pydicom
import pyocr
from PIL import Image, ImageChops, ImageFilter


digits_dict = {
    ".": [3, 3, 0, 0, 0, 0],
    "0": [10, 4, 2, 2, 4, 10],
    "1": [1, 12, 0, 0, 0, 0],
    "2": [5, 5, 5, 4, 6, 5],
    "3": [4, 4, 3, 3, 7, 9],
    "4": [2, 4, 4, 4, 12, 1],
    "5": [8, 4, 3, 3, 5, 6],
    "6": [10, 6, 3, 3, 6, 7],
    "7": [3, 1, 5, 5, 5, 3],
    "8": [9, 7, 3, 3, 7, 9],
    "9": [7, 6, 3, 3, 6, 10],
    "(": [8, 6, 4, 2],
    "H": [12, 1, 1, 1, 1, 12],
    "e": [6, 5, 3, 3, 5, 4],
    "a": [4, 6, 3, 3, 4, 7],
    ")": [2, 4, 6, 8],
    "B": [12, 3, 3, 3, 7, 9],
    "o": [6, 4, 2, 2, 4, 6],
    "d": [6, 4, 2, 2, 2, 12],
    "y": [2, 4, 5, 3, 4, 3]
}


def get_dicom(path: str) -> list:
    """pathを入力し，dicomファイルをリストで返す

    Args:
        path (str): [description]

    Returns:
        list: pydicom.dcmread
    """
    file_to_path = glob.glob(path)
    dicomfiles = [pydicom.dcmread(p) for p in file_to_path]
    return dicomfiles


def get_tesseract(is_dev):
    if is_dev:
        path_tesseract = "C:\\Program Files (x86)\\Tesseract-OCR"
    else:
        path_tesseract = ".\\Resources\\Tesseract-OCR"

    if path_tesseract not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + path_tesseract
    # print(os.environ["PATH"])
    tools = pyocr.get_available_tools()
    tool = tools[0]
    return tool

def find_protocol_OCR(separated_img: np.ndarray, prot_lang: str, use_tesser:bool ,tool=None):
    """プロトコル名，ヘッダーの場所を検索する

    Args:
        separated_img (np.ndarray): np_img
        tool (module): [description]
        prot_lang (str):protocol lang

    Returns:
    protocol_list
            list: {
                "protocol":n
                },
                {
                "protocol":n
                }

    header_index
            list

    """
    header_index = []
    protocol_list = []
    if use_tesser:
        # 以下のパターンをプロトコル名として認識
        prot_pattern = "(\d\.*)"
        if prot_lang=='jpn':
            header_pattern = "トータル"
        else:
            header_pattern = "Total"
        # result_list = []
        for i, s_i in enumerate(separated_img):
            img_org_sp = Image.fromarray(s_i)
            img_org_sp_crop = cropImage(img_org_sp)
            m_5 = 5
            img_org_sp_crop_margin_5 = add_margin(
                img_org_sp_crop, m_5, m_5, m_5, m_5)

            m_10 = 10
            img_org_sp_crop_margin_10 = add_margin(
                img_org_sp_crop, m_10, m_10, m_10, m_10)
            # img_org_sp_crop_margin.show()

            # Assume a single column of text of variable sizes.
            builder = pyocr.builders.TextBuilder(tesseract_layout=4)

            result_5 = tool.image_to_string(
                img_org_sp_crop_margin_5, lang=prot_lang, builder=builder)
            result_10 = tool.image_to_string(
                img_org_sp_crop_margin_10, lang=prot_lang, builder=builder)

            # print(result)
            # result_list.append(result)
            repatter = re.compile(prot_pattern)
            rst_5 = repatter.match(result_5)
            rst_10 = repatter.match(result_10)

            if (header_pattern in result_5) or (header_pattern in result_10):
                header_index.append(i)

            if not (rst_5 or rst_10) is None:
                if rst_5 is None:
                    tmp_dict = {str(result_10): i}
                elif rst_10 is None:
                    tmp_dict = {str(result_5): i}

                elif not (rst_5 and rst_10) is None:
                    tmp_dict = {str(result_10): i}
                protocol_list.append(tmp_dict)

    else:
        json_path = "./Resources/PROTOCOL_PROJECTION.json"
        json_data = open(json_path,mode='r',encoding='utf-8')
        json_projection_data = json.load(json_data)
        json_data.close()
        
        for i, s_i in enumerate(separated_img):
            # ndarray >>> PIL
            img_org_sp = Image.fromarray(s_i)
            # crop image
            img_org_sp_crop = cropImage(img_org_sp)
            # PIL >>> ndarray
            np_img = np.array(img_org_sp_crop)
            
            # Convert 1 >> 0, 255 >> 1
            np_img = np.where(np_img==1, 0, 1)
            # 縦方向にデータを加算する
            np_sum = np_img.sum(axis=0)
            # array >>> list
            np_sum_list = list(np_sum)
            
            projection_str = ''
            for sum in np_sum_list:
                projection_str += str(sum)
            
            
            """
            projection_str = "1.ABC"
            scanName1 = "AB"
            scanName2 = "ABC"
            のとき、scanName2が正解であるはずだが、for文を回したときに、
            scanName1が先に取得され、正解だと判定されてしまう。
            そこで、正解の候補をcandidate_protocolに格納し、最後に類似度で判定する。
            """
                    
            candidate_protocol = []
            
            # jsonに登録されているデータと読み取った結果を照合する
            for key in json_projection_data[0]:
                value = json_projection_data[0][key]
                
                # dose header (トータルMAS, 照射時間,,,)
                if (value in projection_str) and key=="dose_header":
                    header_index.append(i)
                
                # 登録されているプロトコル名とマッチした場合
                elif value in projection_str: #FIXME: protocol
                    tmp_dict = {key: i}
                    candidate_protocol.append(tmp_dict)
                    
                else:
                    pass
            
            # candidate_protocol が空のとき、エラーになるため、except
            try:
                # Levenshtein distance
                def calc_dist(candidate_Scanname):
                    scanname = [k for k in candidate_Scanname.keys()][0]
                    # projectiondataを取り出す
                    default = json_projection_data[0][scanname]
                    # 距離を求める
                    lev_dist = Levenshtein.distance(projection_str, default)
                    devider = len(projection_str) if len(projection_str) > len(default) else len(default)
                    lev_dist = lev_dist / devider
                    lev_dist = 1 - lev_dist
                    return lev_dist
                
                # candidate_protocol から距離をそれぞれ求める
                dist = list(map(calc_dist, candidate_protocol))
                # index を返す
                lev_index = dist.index(max(dist))
                # プロトコル名を返す
                resultProtocol = candidate_protocol[lev_index]
                protocol_list.append(resultProtocol)
            except Exception as e:
                # print(e)
                pass
            
        
    return protocol_list, header_index


def sepatateImage(croped_np: np.ndarray) -> list:
    """np imageを行ごとに分割する
        空白行を探し出し、横長に画像を切り出していく。

    Args:
        croped_np (np.ndarray): [description]

    Returns:
        list: [np.ndarray] separated_img
    """
    h, _ = croped_np.shape

    blk_list = []  # 空白行を格納する
    for i in range(h):
        if croped_np[i, :].max() == 1:
            blk_list.append(i)

    tmp_list_max = []  # 空白行の最大値を格納
    for i, b in enumerate(blk_list):
        try:
            if(blk_list[i+1]-b) == 1:
                pass
            else:
                tmp_list_max.append(b)
        except:
            tmp_list_max.append(b)  # 最終行はエラーになるため，ここで代入

    tmp_list_min = []  # 空白行の最大値を格納
    for i, b in enumerate(blk_list):
        try:
            if(b - blk_list[i-1]) == 1:
                pass
            else:
                tmp_list_min.append(b)
        except:
            tmp_list_min.append(b)  # 最初の行はエラーになるため，ここで代入

    # 空白行の中間の値を取得
    borders = [int((x+y)/2) for (x, y) in zip(tmp_list_max, tmp_list_min)]

    separated_img = []
    sep_cnt = 0
    try:
        # print(borders)
        for border in borders:
            separated_img.append(croped_np[sep_cnt:border, :])
            sep_cnt = border
        # 最後は以下のプログラムで追加
        separated_img.append(croped_np[sep_cnt:, :])
    except:
        pass

    return separated_img


def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), 1)
    result.paste(pil_img, (left, top))
    return result


def cropImage(img):
    """Crop

    Args:
        img (PIL.Image.Image): [description]

    Returns:
        [PIL.Image.Image]: [description]
    """
    # 画像と同じサイズの空画像を作成
    bg = Image.new("L", img.size, img.getpixel((0, 0)))
    # 差分画像を生成
    diff = ImageChops.difference(img, bg)
    # 背景色との境界を求めて切り抜く. 画像内で値が0でない最小領域を返す
    croprange = diff.convert("L").getbbox()
    crop_img = img.crop(croprange)

    return crop_img


def ocr_with_crop(np_img, tool):
    """ScanName, 線量情報をOCRで読み取る。
    tool=None のときはProjectionデータから、そうでないときはTesseractから読み取る.

    Args:
        np_img ([type]): [description]
        tool ([type]): [description]

    Returns:
        [list]: output from Tesseract
    """
    result_list = []

    img_org_sp = Image.fromarray(np_img)
    img_org_sp_crop = cropImage(img_org_sp)
    img_org_sp_crop_margin = add_margin(img_org_sp_crop, 5, 5, 5, 5)
    try:
        # Dilate 3 times to prepare for Separate image
        dilation = img_org_sp_crop_margin.filter(ImageFilter.MaxFilter())
        dilation = dilation.filter(ImageFilter.MaxFilter())
        dilation = dilation.filter(ImageFilter.MaxFilter())
        # dilation.show()
    except Exception as e:
        print(e)

    # Separate Image by each block to read correctory

    dilation_np = np.array(dilation)
    img_org_sp_crop_margin_np = np.array(img_org_sp_crop_margin)
    _, w = dilation_np.shape

    blk_list = []  # 空白行を格納する
    # Run for row
    for i in range(w): # TODO: 微分
        if dilation_np[:, i].max() == 1:
            blk_list.append(i)
    tmp_list_max = []  # 空白行の最大値を格納
    for i, b in enumerate(blk_list):
        try:
            if(blk_list[i+1]-b) == 1:
                pass
            else:
                tmp_list_max.append(b)
        except:
            tmp_list_max.append(b)  # 最終行はエラーになるため，ここで代入

    tmp_list_min = []  # Store max index of blank row
    for i, b in enumerate(blk_list):
        try:
            if(b - blk_list[i-1]) == 1:
                pass
            else:
                tmp_list_min.append(b)
        except:
            tmp_list_min.append(b)  # Because of error, first row append here
    # Get center of blank index
    borders = [int((x+y)/2) for (x, y) in zip(tmp_list_max, tmp_list_min)]

    separated_img = []
    sep_cnt = 0
    try:
        # print(borders)
        for border in borders:
            separated_img.append(img_org_sp_crop_margin_np[:, sep_cnt:border])
            sep_cnt = border
        # add Final img
        separated_img.append(img_org_sp_crop_margin_np[:, sep_cnt:])
    except:
        pass

    # remove first and last separated image because these are black tile
    try:
        separated_img = separated_img[1:-1]
    except:
        pass

    for i, img in enumerate(separated_img):
        # ScanName
        if i == 0:
            if tool!=None:
                img_org_sp = Image.fromarray(img)
                img_org_sp_crop = cropImage(img_org_sp)
                img_org_sp_crop_margin = add_margin(img_org_sp_crop, 5, 5, 5, 5)
                # Call Tesseract
                builder_DoseInfo = pyocr.builders.TextBuilder(tesseract_layout=4)
                builder_DoseInfo.tesseract_configs.append("digits")
                scanName = tool.image_to_string(
                    img_org_sp_crop_margin, lang="eng", builder=builder_DoseInfo)
                result_list.append(scanName)
            else:
                # TODO: ScannameのProjection dataを作成する
                # jsonを読み込み
                json_path = "./Resources/SCANNAME_PROJECTION.json"
                json_data = open(json_path,mode='r',encoding='utf-8')
                json_projection_data = json.load(json_data)
                json_data.close()
                
                
                for i, s_i in enumerate(separated_img):
                    # ndarray >>> PIL
                    img_org_sp = Image.fromarray(s_i)
                    # crop image
                    img_org_sp_crop = cropImage(img_org_sp)
                    # PIL >>> ndarray
                    np_img = np.array(img_org_sp_crop)
                    
                    # Convert 1 >> 0, 255 >> 1
                    np_img = np.where(np_img==1, 0, 1)
                    # 縦方向にデータを加算する
                    np_sum = np_img.sum(axis=0)
                    # array >>> list
                    np_sum_list = list(np_sum)
                    
                    # 読み取った結果を羅列する.
                    projection_str = ''
                    for sum in np_sum_list:
                        projection_str += str(sum)
                    
                    
                    # jsonに登録されているデータと読み取った結果を照合する
                    for scanName in json_projection_data[0]:
                        value = json_projection_data[0][scanName]
                        
                        # 登録されているプロトコル名とマッチした場合
                        if value in projection_str:
                            result_list.append(scanName)
                            
                        else:
                            pass
                    
                    
                    
        # 数値情報
        else:
            # Identification Digits or Letters
            returned_digits = read_digits(img)
            result_list.append(returned_digits)

    return result_list


def read_digits(np_img) -> str:
    # np >> PIL
    img_org_sp = Image.fromarray(np_img)
    # Crop
    img_org_sp_crop = cropImage(img_org_sp)

    # PIL >> np
    np_img = np.array(img_org_sp_crop)

    # Convert 1 >> 0, 255 >> 1
    np_img = np.where(np_img == 1, 0, 1)
    # sumup axis=0 and get projection data
    np_sum = np_img.sum(axis=0)
    # add projection data ile into projection
    each_projection = []
    templist = []
    for n in np_sum:
        if n == 0:
            if templist != []:
                each_projection.append(templist)
                templist = []
            else:
                pass
        else:
            templist.append(n)
    if templist != []:
        each_projection.append(templist)
    else:
        pass

    # Identification digits or letters
    result_digit = ""
    for proj in each_projection:
        if proj == [3, 3]:
            result_digit = result_digit + "."
        elif proj == [10, 4, 2, 2, 4, 10]:
            result_digit = result_digit + "0"
        elif proj == [1, 12]:
            result_digit = result_digit + "1"
        elif proj == [5, 5, 5, 4, 6, 5]:
            result_digit = result_digit + "2"
        elif proj == [4, 4, 3, 3, 7, 9]:
            result_digit = result_digit + "3"
        elif proj == [2, 4, 4, 4, 12, 1]:
            result_digit = result_digit + "4"
        elif proj == [8, 4, 3, 3, 5, 6]:
            result_digit = result_digit + "5"
        elif proj == [10, 6, 3, 3, 6, 7]:
            result_digit = result_digit + "6"
        elif proj == [3, 1, 5, 5, 5, 3]:
            result_digit = result_digit + "7"
        elif proj == [9, 7, 3, 3, 7, 9]:
            result_digit = result_digit + "8"
        elif proj == [7, 6, 3, 3, 6, 10]:
            result_digit = result_digit + "9"
        elif proj == [8, 6, 4, 2]:
            result_digit = result_digit + "("
        elif proj == [12, 1, 1, 1, 1, 12]:
            result_digit = result_digit + "H"
        elif proj == [6, 5, 3, 3, 5, 4]:
            result_digit = result_digit + "e"
        elif proj == [4, 6, 3, 3, 4, 7]:
            result_digit = result_digit + "a"
        elif proj == [2, 4, 6, 8]:
            result_digit = result_digit + ")"
        elif proj == [12, 3, 3, 3, 7, 9]:
            result_digit = result_digit + "B"
        elif proj == [6, 4, 2, 2, 4, 6]:
            result_digit = result_digit + "o"
        elif proj == [6, 4, 2, 2, 2, 12]:
            result_digit = result_digit + "d"
        elif proj == [2, 4, 5, 3, 4, 3]:
            result_digit = result_digit + "y"
        else:
            img_org_sp_crop.show()
    return result_digit


def get_info_from_prot(protocol_list: list, header_index: list, separated_img, tool):
    """[summary]

    Args:
        protocol_list (list): {"protocol":index},{},{},...
        header_index (list) : header index
        separated_img (list): [description]
        tool (module): [description]

    out_list:
        [list]: [
            {"protocol":[Dose Info]},
            {"protocol":[Dose Info]},
            {"protocol":[Dose Info]}
            ]
    """
    out_list = []

    index_of_all_protocol = []  # protocol名が位置するindexの値
    
    # プロトコル名を目印に読み取る場所を確定するため、全てのプロトコルの場所を格納する
    for prot_dict in protocol_list:
        # index を取り出す
        idx = [i for i in prot_dict.values()][0]
        index_of_all_protocol.append(idx)
        

    # for pro in prot_dict.keys():
    #     i = prot_dict[pro]
    #     prot_index.append(i)

    for i, protocol_dict in enumerate(protocol_list):
        key = [k for k in protocol_dict.keys()][0]
        p = index_of_all_protocol[i]
        dose_list = []

        if p != 'ex_protocol':
            try:
                start = p + 2
                end = index_of_all_protocol[i+1]
                for d in range(end-start):
                    re_read_img = separated_img[start + d]
                    result = ocr_with_crop(re_read_img, tool)
                    dose_list.append(result)

            except Exception as e:
                start = p + 2
                end = len(separated_img)

                for d in range(end-start):
                    re_read_img = separated_img[start + d]
                    result = ocr_with_crop(re_read_img, tool)
                    dose_list.append(result)

        # protocol名が見つからず，ex_protocolを利用する場合
        else:
            try:
                start = header_index[0] + 1
                end = len(separated_img)

                for d in range(end-start):
                    re_read_img = separated_img[start + d]
                    result = ocr_with_crop(re_read_img, tool)
                    dose_list.append(result)
            except:
                pass

        tmp_dict = {key: dose_list}
        out_list.append(tmp_dict)

    return out_list


def ocr(dicomfile, prot_lang, use_tesser, tool=None, ex_protocol=None):
    # pydicom(ndarray;uint16) >>> ndarray;uint8 に変換
    pix_np_array = np.array(dicomfile.pixel_array, dtype='uint8')
    # ndarray;uint8 >>> PIL に変換
    img_org = Image.fromarray(pix_np_array)
    #上下左右をトリミング
    crop_img = cropImage(img_org) 
    # PIL >>> ndarray;uint8　に変換
    crop_np = np.array(crop_img)
    # 画像を行ごとに分割
    separated_img = sepatateImage(crop_np)
    protocol_list, header_index = find_protocol_OCR(separated_img, prot_lang, use_tesser, tool=tool)

    if (len(protocol_list)==0) and (ex_protocol != None):
        protocol_list = [{ex_protocol: "ex_protocol"}]

    out_list = get_info_from_prot(protocol_list, header_index, separated_img, tool)
    return out_list, header_index


def replace_and_split(out_dict: dict) -> dict:
    """文字を正規化する

    Args:
        out_dict (dict): {
            protocol:list(Data1, Data2,...),
            protocol:list(Data1, Data2,...),
        }

    Returns:
        dict: {
            protocol:list(list(Data1), list(Data2),...),
            protocol:list(list(Data1), list(Data2),...)
        }
    """
    for prot in out_dict.keys():
        valuelist = out_dict[prot]
        for i, v_l in enumerate(valuelist):
            # print(v_l)
            v_l = v_l.replace(', ', '.').replace(
                ',', '.').replace('. ', '.').replace(' (', '(')
            v_l = v_l.split(' ')

            # 2文字以下の異常検出を削除
            if len(v_l) < 6:
                pass
            else:
                for v in v_l:
                    if len(v) < 3:
                        v_l.remove(v)

            valuelist[i] = v_l
        out_dict[prot] = valuelist
    return out_dict


def calc_Levenshtein(str1: str, default_list: list) -> tuple:
    """Levenshtein距離を測り，2つの結果をタプルで返す.

    Args:
        str1 (str): OCRで読み取られたプロトコル名
        default_list (list): ユーザーが登録したプロトコル名

    Returns:
        tuple: Levenshtein, jaro_winklerのそれぞれの結果
    """
    p = str1[2:]

    def main(default):
        # jaro_winkler
        jaro_dist = Levenshtein.jaro_winkler(p, default)

        # ゲシュタルトパターンマッチング
        gestalt1 = difflib.SequenceMatcher(None, p, default).ratio()
        gestalt2 = difflib.SequenceMatcher(None, default, p).ratio()

        # Levenshtein distance
        lev_dist = Levenshtein.distance(p, default)
        devider = len(p) if len(p) > len(default) else len(default)
        lev_dist = lev_dist / devider
        lev_dist = 1 - lev_dist
        return lev_dist, jaro_dist, gestalt1, gestalt2

    dist = list(map(main, default_list))
    # lev_dist = list(map(main, default_list))

    # 2つの結果をベクトルとみなし，合計ベクトルが最大のインデックスを返す
    dist_point = list(
        map(lambda x: (x[0]**2+x[1]**2+x[2]**2+x[3]**2)**0.5, dist))
    lev_index = dist_point.index(max(dist_point))

    # d_protocol = str1[:2] + default_list[lev_index]  # プロトコル番号 n. を表示する場合
    d_protocol = default_list[lev_index]  # プロトコル番号 n. を表示しない

    # d_protocol = default_list[lev_index] #プロトコル名のみ

    # print("{} , {}".format(d_protocol, lev_dist[lev_index]))
    return d_protocol
