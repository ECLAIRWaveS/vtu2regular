# Convert unstructured VTU data to regular gridded data

Uses the [VTK](https://vtk.org/) library to convert unstructured data in .vtu files to regular gridded data.

Install this (and prerequisite Python modules) in development "live" mode by:

```sh
pip install -e ./vtu2regular
```

## Usage

```sh
python -m vtu2regular ~/my.vtu ~/out/my.h5
```

## Reference

[general Python VTK examples](https://examples.vtk.org/site/Python/)
[VTK Pipeline examples](https://github.com/boryszef/vtk-python-examples/blob/master/080_function_gradient2.py)
