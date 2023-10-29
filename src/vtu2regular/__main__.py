import argparse

from . import read_vtu, regularize, write_reg

p = argparse.ArgumentParser(description="Convert .vtu to regular grid")
p.add_argument("vtu_file", help=".vtu file to convert")
p.add_argument("output_file", help="output file name", nargs="+", default=None)
P = p.parse_args()

raw, nodes = read_vtu(P.vtu_file)

reg = regularize(raw, nodes)

write_reg(reg, P.output_file)
