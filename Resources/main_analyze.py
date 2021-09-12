import argparse

from cython_modules import analyze


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="show statistics")
    parser.add_argument("--target", help="CTDIvol or DLP")
    parser.add_argument("--modality", help="modality   ex) '('CT', 'PT')' ")
    args = parser.parse_args()

    target = args.target
    modality = args.modality

    analyze.main(target=target, modality=modality)
