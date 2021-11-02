import argparse
import os
import sys
import time

sys.path.append(os.getcwd() + "\\donuts_env\\Lib\\site-packages")

import numpy as np
import pydicom
from PIL import Image


def main(path: str):
    timeString = str(time.time())
    try:
        dicomfile = pydicom.dcmread(path)
    except Exception as e:
        print(e)

    txtname = "./Resources/temp/" + timeString + "_dicomtext.txt"

    with open(txtname, 'w') as f:
        print(dicomfile, file=f)

    try:
        pix_np_array = np.array(dicomfile.pixel_array, dtype='uint8')
        img_org = Image.fromarray(pix_np_array)
        picName = "./Resources/temp/" + timeString + "_low_data.png"
        img_org.save(picName)
    except:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="path")
    parser.add_argument("--path", help="dicom path.")
    args = parser.parse_args()

    path = args.path

    main(path)
