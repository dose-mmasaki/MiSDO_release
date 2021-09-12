import argparse
from cython_modules import out_csv

"""
SQLを引数にCSVを出力する
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SQLを受け取り，DBからCSVを出力する.")
    parser.add_argument("--sql", help="SELECT文を入力")
    args = parser.parse_args()
    try:
        sql = args.sql
        sql="SELECT * FROM ALL_DATA"
        out_csv.main(sql)
    except Exception as e:
        print(e)