import argparse

from cython_modules import show_low_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="path")
    parser.add_argument("--path", help="dicom path.")
    args = parser.parse_args()
    
    path = args.path


    show_low_data.main(path)
