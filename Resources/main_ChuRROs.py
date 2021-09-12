# -*- coding: utf-8 -*-

import argparse
import time
from cython_modules import ChuRROs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get language of Protocol. input 'jpn' or 'eng' ")
    parser.add_argument("--lang", help="Language of Protocol.")
    parser.add_argument("--dev", help="Developer mode? Anser 'yes'")
    args = parser.parse_args()
    
    prot_lang = args.lang
    is_dev = args.dev

    
    if is_dev == 'yes':
        is_dev=True
        prot_lang = 'jpn'
    else:
        is_dev=False

        
    result = ChuRROs.main(prot_lang=prot_lang, is_dev=is_dev)
    

    ChuRROs.writeDB_from_list('OCR',result)
    
    print("This program will end in 10 seconds")
    time.sleep(10)
