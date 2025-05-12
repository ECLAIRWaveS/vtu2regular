from pathlib import Path

import scipy.interpolate as interp

import vtk
from vtk.util.numpy_support import vtk_to_numpy

import numpy as np

from scipy.interpolate import griddata as griddata

import h5py

import gemini3d.coord
# from vtk.numpy_interface import dataset_adapter as dsa

__version__ = "0.0.1"
Re = 6370e3


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


def sample_gemini(data, centers, parmids=[-1], lpts=None, lims=None, targettype=None):
    """
    sample unstructured data to regular grid

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
    """

    # Set defaults if needed
    if lpts is None:
        lpts=[128,128,128]
        print("sample_gemini --> default size of ",lpts)
    if targettype is None or not (targettype=="geomgagnetic" or targettype=="geographic"):
        targettype="geomagnetic"
        print("sample_gemini --> defaulting to target geomagnetic coordinates")

    # source coordinates, assume Cartesian or commensurate units at the least.
    x=centers[:,0]
    y=centers[:,1]
    z=centers[:,2]   
    
    # express the source coordinates (which are Cartesian ECEF magnetic in terms
    #   of magnetic latitude and longitude OR geographic lat and lon
    r=np.sqrt(x**2+y**2+z**2)
    #rho=np.sqrt(x**2+y**2)
    theta=np.arccos(np.minimum(np.maximum(z/r,-1),1))
    phi=np.arctan2(y,x)
    alt=r-Re
     
    if targettype=="geographic":
        print("sample_gemini --> Target coords. are geographic")
        lat,lon = gemini3d.coord.geomag2geog(theta, phi)
    else: 
        print("sample_gemini --> Target coords. are geomagnetic")
        lat=90-theta*180/np.pi
        lon=phi*180/np.pi
        
    # Now that the source coords have been expressed in the target system we can
    #   define extents.  
    if lims is None:
        lims=[alt.min(),alt.max(),lon.min(),lon.max(),lat.min(),lat.max()]
        print("sample_gemini --> defaulting to min/max based on source grid limits")   
        
    # create a gridded target set of interpolate sites; target coordinate system
    #   is either geomagnetic or geographic per user input
    x1i=np.linspace(lims[0],lims[1],lpts[0])       # altitude
    x2i=np.linspace(lims[2],lims[3],lpts[1])       # mag. or geog. lon.
    x3i=np.linspace(lims[4],lims[5],lpts[2])       # mag. or geog. lat.
    [X1i,X2i,X3i]=np.meshgrid(x1i,x2i,x3i,indexing="ij")

    # convert interpolation sites to source coordinate system.  Arguably these types
    #   of transformations should be calls to gemini3d.coord even though they are
    #   quite simple
    Ri=X1i+Re
    if targettype=="geographic":
        THETAi,PHIi = gemini3d.coord.geog2geomag(X3i,X2i)
    else:
        THETAi=np.pi/2-X3i*np.pi/180
        PHIi=X2i*np.pi/180           
    Zi=Ri*np.cos(THETAi)
    Xi=Ri*np.sin(THETAi)*np.cos(PHIi)
    Yi=Ri*np.sin(THETAi)*np.sin(PHIi)

    # which parameters are we needing to grid
    if parmids[0]==-1:                           # extract all parameters
        parmidextract=range(0,data.shape[1])     # second axis is parameter number
        print("sample_gemini --> WARNING:  extracting and gridding all parameters.  May take a while...")
    else: 
        parmidextract=parmids            # extract only a set number of parameters

    # perform interpolation onto target sites
    parmi=np.zeros( (lpts[0], lpts[1], lpts[2], len(parmidextract) ), dtype=np.float32 )
    for iparm in range(len(parmidextract)):
        print("sample_gemini --> Sampling parameter number:  ",parmidextract[iparm]," on target grid size ",lpts)
        parmitmp = griddata((x,y,z), data[:,parmidextract[iparm]], (Xi.flatten(order="F"),Yi.flatten(order="F"),Zi.flatten(order="F")),method="nearest")
        parmi[:,:,:,iparm]=parmitmp.reshape(lpts,order="F")
        
    return x1i,x2i,x3i,parmi


def sample_gemini_2D(data, centers, parmids=[-1], lpts=None, lims=None, targettype=None):
    """
    Sample unstructured data to regular grid.  The source coordinate system is rho,z where
    rho = sqrt(x**2 + y**2), and x,y,z are ECEF magnetic coordinates.  

    https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
    """

    # Set defaults if needed
    if lpts is None:
        lpts=[128,128]
        print("sample_gemini --> default size of ",lpts)
    targettype="geomagnetic"     # force geomagnetic  always for 2D ouptut
    print("sample_gemini --> target geomagnetic coordinates...")

    # source coordinates, assume Cartesian or commensurate units at the least.
    rho=centers[:,0]
    z=centers[:,1]
    _=centers[:,2]      # for 2D Trees GEMINI output this should be all zeros, always
     
    print("sample_gemini --> Target coords. are geomagnetic")
    r=np.sqrt(rho**2+z**2)
    theta = np.arccos(np.minimum(np.maximum(z/r,-1),1))
    alt=r-Re
    lat=90-theta*180/np.pi
        
    # Now that the source coords have been expressed in the target system we can
    #   define extents.  
    if lims is None:
        lims=[alt.min(),alt.max(),lat.min(),lat.max()]
        print("sample_gemini --> defaulting to min/max based on source grid limits")   
        
    # create a gridded target set of interpolate sites; target coordinate system
    #   is either geomagnetic or geographic per user input
    x1i=np.linspace(lims[0],lims[1],lpts[0])       # altitude
    x2i=np.linspace(lims[2],lims[3],lpts[1])       # mag. lat.
    [X1i,X2i]=np.meshgrid(x1i,x2i,indexing="ij")

    # convert interpolation sites to source coordinate system.  Arguably these types
    #   of transformations should be calls to gemini3d.coord even though they are
    #   quite simple
    Ri=X1i+Re
    THETAi=np.pi/2-X2i*np.pi/180
    Zi=Ri*np.cos(THETAi)
    RHOi=Ri*np.sin(THETAi)

    # which parameters are we needing to grid
    if parmids[0]==-1:                           # extract all parameters
        parmidextract=range(0,data.shape[1])     # second axis is parameter number
        print("sample_gemini --> WARNING:  extracting and gridding all parameters.  May take a while...")
    else: 
        parmidextract=parmids            # extract only a set number of parameters

    # perform interpolation onto target sites
    parmi=np.zeros( (lpts[0], lpts[1], len(parmidextract) ), dtype=np.float32 )
    for iparm in range(len(parmidextract)):
        print("sample_gemini --> Sampling parameter number:  ",parmidextract[iparm]," on target grid size ",lpts)
        parmitmp = griddata((rho,z), data[:,parmidextract[iparm]], (RHOi.flatten(order="F"),Zi.flatten(order="F")),method="nearest")
        parmi[:,:,iparm]=parmitmp.reshape(lpts,order="F")
        
    return x1i,x2i,parmi



def write_sampled(x1i,x2i,x3i,coordlbls,parmi,parmlbls,file: Path):
    """
    write regular grid and data to an hdf5 file
    """
    
    f = h5py.File(file,"w")
    f.create_dataset("/x1i",data=x1i)
    f.create_dataset("/x2i",data=x2i)
    f.create_dataset("/x3i",data=x3i)
    f.create_dataset("/coordlbls",data=coordlbls)
    f.create_dataset("/parmi",data=parmi)
    f.create_dataset("/parmlbls",data=parmlbls)
    f.close()
    
    return 


