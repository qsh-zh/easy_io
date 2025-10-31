import argparse

import easy_io

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs="+")
args = parser.parse_args()


def simple():
    for i, filename in enumerate(args.filename):
        globals()[f"f{i + 1}"] = easy_io.load(filename)

    from IPython import embed

    embed()
