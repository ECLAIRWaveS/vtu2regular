#!/usr/bin/env python3
"""
NOTE: it appears VTK Python interface may not yet support VTKHDF files.
"""

import argparse
from pathlib import Path

import vtk


def read_vtk(file: Path):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(file)
    reader.Update()

    return reader.GetOutput()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Read VTKHDF file")
    p.add_argument("vtk_file", help="VTK file to read")
    P = p.parse_args()

    file = Path(P.vtk_file).expanduser()
    if not file.is_file():
        raise FileNotFoundError(file)

    data = read_vtk(file)
