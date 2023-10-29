from pathlib import Path

import scipy.interpolate as interp

import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.numpy_interface import dataset_adapter as dsa

__version__ = "0.0.1"


def read_vtu(file: Path):
    """
    read .vtu unstructured grid file to Numpy ndarray
    """

    file = Path(file).expanduser()
    if not file.is_file():
        raise FileNotFoundError(file)

    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(file)

    # no longer available methods
    # reader.ReadAllScalarsOn()
    # reader.ReadAllVectorsOn()

    reader.Update()

    usg = dsa.WrapDataObject(reader.GetOutput())
    data = vtk_to_numpy(usg.GetPoints())
    print(f"{file} data shape: {data.shape}")

    return data

    # coordinates of nodes in the mesh
    # nodes_vtk = reader.GetOutput().GetPoints().GetData()
    # print(nodes_vtk)
    # nodes = vtk_to_numpy(nodes_vtk)
    # # print(nodes.shape)

    # output = reader.GetOutput()

    # #Grab a scalar from the vtk file
    # a = output.GetPointData().GetArray()
    # print(a)

    # https://vtk.org/doc/nightly/html/classvtkResampleToImage.html


def regularize(raw):
    """
    convert unstructured grid to regular grid
    """

    interp.NearestNDInterpolator


def write_reg(reg, file):
    """
    write regular grid to file
    """
    pass
