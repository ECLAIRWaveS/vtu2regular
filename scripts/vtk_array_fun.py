#!/usr/bin/env python3
"""
Instantiate a VTK array and fill it with data.
"""

import vtk
import numpy as np

# make 3 x 4 array
A = np.arange(12).reshape(3, 4)

V = vtk.vtkDoubleArray()

if A.ndim < 2:
    V.SetNumberOfComponents(1)
    V.SetNumberOfTuples(A.size)
else:
    # A.size must be even
    if A.size % A.T.shape[0] != 0:
        raise ValueError("First array dimension must evenly divide A.size")

    V.SetNumberOfComponents(A.T.shape[0])
    V.SetNumberOfTuples(A.size//A.T.shape[0])
    V.SetVoidArray(A, A.size, 1)
