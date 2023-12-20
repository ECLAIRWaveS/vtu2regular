from pathlib import Path

import scipy.interpolate as interp

import vtk
from vtk.util.numpy_support import vtk_to_numpy
# from vtk.numpy_interface import dataset_adapter as dsa

__version__ = "0.0.1"


def read_vtu(file: Path) -> tuple:
    """
    read .vtu unstructured grid file to Numpy ndarray
    """

    file = Path(file).expanduser()
    if not file.is_file():
        raise FileNotFoundError(file)

    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(str(file))

    # not available for UnstructuredReader
    # reader.ReadAllScalarsOn()
    # reader.ReadAllVectorsOn()

    reader.Update()
    output = reader.GetOutput()

    # just returns grid points as following code
    # usg = dsa.WrapDataObject(reader.GetOutput())
    # data = vtk_to_numpy(usg.GetPoints())

    # coordinates of nodes in the mesh; not sure what "nodes" are...
    nodes_vtk = output.GetPoints().GetData()
    # print(nodes_vtk)
    nodes = vtk_to_numpy(nodes_vtk)

    # MZ - I believe this may be the cell index data; into what I'm not sure
    #cellctridx=vtk_to_numpy(output.GetCellLocationsArray())
    
    # use a filter to retrieve cell centers
    #cellctrsdata=vtk.vtkDoubleArray()
    cellctrs=vtk.vtkCellCenters()
    cellctrs.SetInputDataObject(output)
    cellctrs.Update()
    cellctrsdata=cellctrs.GetOutput()
    ctrs=vtk_to_numpy(cellctrsdata.GetPoints().GetData())
    
    # The below line to compute the cell centers will segfault
    #cellctrs.ComputeCellCenters(output,cellctrsdata)

    data = vtk_to_numpy(output.GetCellData().GetArray("meqn"))
       
    return data, ctrs, nodes

    # a = output.GetPointData().GetArray()

    # https://vtk.org/doc/nightly/html/classvtkResampleToImage.html


def regularize(raw, nodes):
    """
    convert unstructured grid to regular grid

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
    """

    interp.griddata

    return None


def write_reg(reg, file: Path):
    """
    write regular grid to file
    """
    pass
