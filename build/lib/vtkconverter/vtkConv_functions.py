""""
########################################################################################################
# Copyright 2022 F4E | European Joint Undertaking for ITER and the Development                         #
# of Fusion Energy (‘Fusion for Energy’). Licensed under the EUPL, Version 1.2                         #
# or - as soon they will be approved by the European Commission - subsequent versions                  #
# of the EUPL (the “Licence”). You may not use this work except in compliance                          #
# with the Licence. You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl.html       #
# Unless required by applicable law or agreed to in writing, software distributed                      #
# under the Licence is distributed on an “AS IS” basis, WITHOUT WARRANTIES                             #
# OR CONDITIONS OF ANY KIND, either express or implied. See the Licence permissions                    #
# and limitations under the Licence.                                                                   #
########################################################################################################
"""

# CODE: vtkConv_functions (module used in conjunction with vtkconverter)

# LANGUAGE: PYTHON 3.9

# AUTHOR/S: Xavier Mosquera

# e-MAIL/S: xavier.mosquera@estudiantat.upc.edu

# DATE: 31/01/2022

# Copyright F4E 2022

# IDM: F4E_D_2RCXX3 v1.0

import pyvista as pv
import numpy as np
import csv
import tkinter

from copy import deepcopy
from tqdm import tqdm
from tkinter import filedialog


# CLASS DEFINITION
class MeshTally:
    def __init__(self, fn):  # file name
        self.filename = fn
        self.mesh = pv.read(fn)

        self.__readFileInfo__()
        self.__readMeshInfo__()  # call this function to rewrite the mesh attributes after a change

    def __readFileInfo__(self):
        try:
            self.author = self.mesh['author']
            self.host = self.mesh['host']
            self.path = self.mesh['path']
        except:
            pass

    def __readMeshInfo__(self):
        self.centers = self.mesh.cell_centers().points
        self.points = self.mesh.points

        self.cells_info = list(self.mesh.cell_data)  # List of arrays associated to cells
        self.points_info = list(self.mesh.point_data)  # List of arrays associated to points

        self.n_coordinates = self.points.shape[1]  # Number of dimensions
        self.mesh_type = str(type(self.mesh)).split('.')[-1][:-2]


# END OF CLASS DEFINITION


# GLOBAL VARIABLES DEFINITION

meshtals = dict()  # Here is where all MeshTally objects are saved. The key of each object (value) is its filename

scale_factor = 1  # Defect value is 1
safety_factor = 1  # Defect value is 1


# END OF GLOBAL VARIABLES DEFINITION


# FUNCTION DEFINITIONS

# GET IF AN ARRAY IS ASSOCIATED TO EITHER POINTS OR CELLS
def GetArrayType(meshtal, array_name):
    if array_name in meshtal.cells_info:
        return 'cells'

    elif array_name in meshtal.points_info:
        return 'points'

    else:
        return 'Invalid'


# OPEN A FILE
def Open():
    root = tkinter.Tk()
    root.wm_withdraw()  # This completely hides the root window
    filename_path = tkinter.filedialog.askopenfilename(filetypes=[('vtk files', '.vtk .vts .vtr .vtu')])
    filename = filename_path.split('/')[-1]
    OpenFile(filename)

    root.destroy()


def OpenFile(filename):
    if filename in meshtals:
        print('This file is already open')

    else:
        meshtal = MeshTally(filename)
        meshtals[meshtal.filename] = meshtal  # Open and save the MeshTally object
        # An object is called by its file name
        print('This file has been opened successfully')


# PRINT SOME INFORMATION OF A MESHTALLY OBJECT
def PrintGeneralInfo(meshtal_fn):
    meshtal = meshtals[meshtal_fn]

    dimensions = (meshtal.mesh.bounds[1] - meshtal.mesh.bounds[0],
                  meshtal.mesh.bounds[3] - meshtal.mesh.bounds[2],
                  meshtal.mesh.bounds[5] - meshtal.mesh.bounds[4])

    file = '''
Name: {}
Author: {}
Path: {}
    '''.format(meshtal.filename, meshtal.author, meshtal.path)

    mesh = '''
Number of cells: {}
Number of points: {}
Cells arrays: {}
Points arrays: {}
Number of coordinates: {}
Mesh bounds: {}
Mesh dimensions: {}
Mesh type: {}
    '''.format(meshtal.mesh.n_cells, meshtal.mesh.n_points, str(meshtal.cells_info),
               str(meshtal.points_info), meshtal.n_coordinates, meshtal.mesh.bounds,
               dimensions, meshtal.mesh_type)

    print(file + '\n' + mesh)


def PrintArrayInfo(meshtal_fn, array_name):
    meshtal = meshtals[meshtal_fn]

    if GetArrayType(meshtal, array_name) == 'cells':  # For cells
        min_value = min(meshtal.mesh[array_name])
        max_value = max(meshtal.mesh[array_name])

        integral_no_volume, average_no_volume, integral_volume, average_volume = IntegralAndAverage(meshtal_fn,
                                                                                                    array_name)

        print('''
            Minimum value: {:.2e}
            Maximum value: {:.2e}

            Integral without volume: {:.2e}
            Integral with volume: {:.2e}

            Average without volume: {:.2e}
            Average with volume: {:.2e}
            '''.format(min_value, max_value, integral_no_volume, integral_volume,
                       average_no_volume, average_volume))

    elif GetArrayType(meshtal, array_name) == 'points':  # For points
        min_value = min(meshtal.mesh[array_name])
        max_value = max(meshtal.mesh[array_name])

        integral, average = IntegralAndAverage(meshtal_fn, array_name)

        print('''
            Minimum value: {:.2e}
            Maximum value: {:.2e}

            Integral: {:.2e}
            Average: {:.2e}
            '''.format(min_value, max_value, integral,
                       average))

    else:
        print("This array doesn't belong to neither cells nor points")


def IntegralAndAverage(meshtal_fn, array_name):
    meshtal = meshtals[meshtal_fn]
    # for cells, the volume value is used to calculate the weight of each value of the array

    if GetArrayType(meshtal, array_name) == 'cells':

        integral_no_volume = sum(meshtal.mesh[array_name])
        average_no_volume = integral_no_volume / meshtal.mesh.n_cells

        cells_volume = abs(meshtal.mesh.compute_cell_sizes()['Volume'])
        values = np.multiply(meshtal.mesh[array_name], cells_volume)

        integral_volume = float(sum(values))
        average_volume = integral_volume / sum(cells_volume)

        return integral_no_volume, average_no_volume, integral_volume, average_volume

    else:  # In meshtal.points_info
        integral = sum(meshtal.mesh[array_name])
        average = integral / meshtal.mesh.n_points

        return integral, average


# CHANGE SCALE FACTOR
def ChangeScaleFactor(n):
    global scale_factor
    scale_factor = n

    print('Scale factor = {}'.format(n))


# CHANGE SAFETY FACTOR
def ChangeSafetyFactor(n):
    global safety_factor
    safety_factor = n

    print('Safety factor = {}'.format(n))


# CHANGE COORDINATES SYSTEM
def Translate(meshtal_fn, x=0, y=0, z=0):
    meshtal = meshtals[meshtal_fn]

    if meshtal.mesh_type == 'StructuredGrid' or meshtal.mesh_type == 'UnstructuredGrid':
        new_meshtal = deepcopy(meshtal)

    # The translate function does not work with RectilinearGrid Meshes.
    # So, a RectilinearGrid Mesh must be first converted to StructuredGrid
    elif meshtal.mesh_type == 'RectilinearGrid':
        new_meshtal = ConvertToSG(meshtal)

    else:
        print(' Mesh type must be either RectilinearGrid, StructuredGrid or UnstructuredGrid')
        return

    new_meshtal.mesh.translate((x, y, z))

    new_meshtal.__readMeshInfo__()

    new_name = meshtal.filename[:-4] + '+Trans({},{},{})'.format(x, y, z) + new_meshtal.filename[-4:]
    new_meshtal.filename = new_name
    meshtals[new_name] = new_meshtal

    print("Translation applied successfully. '{}' has been created.".format(new_name))


def Rotate(meshtal_fn, theta_x=0, theta_y=0, theta_z=0):  # Only around one axis. If not, assume order: x --> y --> z
    meshtal = meshtals[meshtal_fn]

    if meshtal.mesh_type == 'StructuredGrid' or meshtal.mesh_type == 'UnstructuredGrid':
        new_meshtal = deepcopy(meshtal)

    # The rotate function does not work with RectilinearGrid Meshes.
    # So, a RectilinearGrid Mesh must be first converted to StructuredGrid
    elif meshtal.mesh_type == 'RectilinearGrid':
        new_meshtal = ConvertToSG(meshtal)

    else:
        print(' Mesh type must be either RectilinearGrid, StructuredGrid or UnstructuredGrid')
        return

    new_meshtal.mesh.rotate_x(theta_x)
    new_meshtal.mesh.rotate_y(theta_y)
    new_meshtal.mesh.rotate_z(theta_z)

    new_meshtal.__readMeshInfo__()

    new_name = meshtal.filename[:-4] + '+Rot({},{},{})'.format(theta_x, theta_y, theta_z) + new_meshtal.filename[-4:]
    new_meshtal.filename = new_name
    meshtals[new_name] = new_meshtal

    print("Rotation applied successfully. '{}' has been created.".format(new_name))


# CONVERT TO STRUCTURED GRID
def ConvertToSG(meshtal):

    sg_meshtal = deepcopy(meshtal)
    sg_meshtal.mesh = meshtal.mesh.cast_to_structured_grid()

    sg_meshtal.__readMeshInfo__()
    sg_meshtal.filename = sg_meshtal.filename[:-4] + '.vts'
    return sg_meshtal


# JOINT TWO MESHTALLY OBJECTS
def JointMesh(meshtal_fn_1, meshtal_fn_2):
    meshtal_1 = meshtals[meshtal_fn_1]
    meshtal_2 = meshtals[meshtal_fn_2]

    j_meshtal = deepcopy(meshtal_1)
    j_meshtal.mesh = meshtal_1.mesh.merge(meshtal_2.mesh)
    # Regardless of the initial meshes, the resulted mesh is an UnstructuredGrid
    j_meshtal.__readMeshInfo__()

    new_name = meshtal_1.filename[:-4] + '+' + meshtal_2.filename[:-4] + '.vtu'
    j_meshtal.filename = new_name

    meshtals[j_meshtal.filename] = j_meshtal
    print("Joint applied to '{}'".format(new_name))


# EXPORT AGAIN TO VTK/VTS/VTR
def ExportMesh(meshtal_fn, out_format):
    meshtal = meshtals[meshtal_fn]

    if out_format == 'binary':
        meshtal.mesh.save(meshtal_fn, binary=True)
        print('Meshtally exported to {} with {} format'.format(meshtal_fn[-3:], out_format))

    elif out_format == 'ascii':
        meshtal.mesh.save(meshtal_fn, binary=False)
        print('Meshtally exported to {} with {} format'.format(meshtal_fn[-3:], out_format))

    else:
        print("Invalid format. It must be: 'binary' or 'ascii'")


# WRITE A FILE IN A CHOSEN FORMAT
def WriteMesh(meshtal_fn, list_array_names, out_format):
    global scale_factor
    global safety_factor
    meshtal = meshtals[meshtal_fn]

    if out_format == 'point_cloud':

        for array_name in list_array_names:
            # multiply the coordinate points chosen by the scale factor and
            # the values of the array selected by the safety factor
            if GetArrayType(meshtal, array_name) == 'cells':  # Take points or centers
                f_points = meshtal.centers * scale_factor
                values = meshtal.mesh[array_name] * safety_factor

            elif GetArrayType(meshtal, array_name) == 'points':
                f_points = meshtal.points * scale_factor
                values = meshtal.mesh[array_name] * safety_factor

            else:
                return 'Invalid array name: {}'.format(array_name)

            new_name = '{}_{}_{}.txt'.format(meshtal.filename[:-4], array_name, out_format)
            f = open(new_name, 'w')
            PointCloud(f, f_points, values)
            print('{} created successfully!'.format(new_name))
            f.close()

    elif out_format == 'ip_fluent':
        for array_name in list_array_names:
            # multiply the coordinate points chosen by the scale factor and
            # the values of the array selected by the safety factor
            if GetArrayType(meshtal, array_name) == 'cells':  # Take points or centers
                f_points = meshtal.centers * scale_factor
                values = meshtal.mesh[array_name] * safety_factor

            elif GetArrayType(meshtal, array_name) == 'points':
                f_points = meshtal.points * scale_factor
                values = meshtal.mesh[array_name] * safety_factor

            else:
                return 'Invalid array name: {}'.format(array_name)

            new_name = '{}_{}_{}.txt'.format(meshtal.filename[:-4], array_name, out_format)
            f = open(new_name, 'w')
            IPFluent(f, meshtal, f_points, values)
            print('{} created successfully!'.format(new_name))
            f.close()

    elif out_format == 'csv':
        # First, ensure all values correspond to either cells or points, and they are the same type
        values_type = GetArrayType(meshtal, list_array_names[0])
        for array_name in list_array_names:
            if GetArrayType(meshtal, array_name) == 'Invalid':
                return 'Invalid array name: {}'.format(array_name)
            elif GetArrayType(meshtal, array_name) != values_type:
                return 'All arrays must correspond to either cells or points.' \
                       ' "{}" corresponds to {} and "{}" to {}'.format(list_array_names[0], values_type,
                                                                       array_name, GetArrayType(meshtal, array_name))
        # multiply the coordinate points chosen by the scale factor
        if values_type == 'cells':  # Take points or centers
            f_points = meshtal.centers * scale_factor

        else:  # Points
            f_points = meshtal.points * scale_factor

        new_name = '{}_{}_{}.csv'.format(meshtal.filename[:-4], str(list_array_names), out_format)
        f = open(new_name, 'w', newline='')
        CSV(f, meshtal, f_points, list_array_names)
        print('{} created successfully!'.format(new_name))
        f.close()

    else:
        print("Invalid format. It must be: 'point_cloud','ip_fluent' o 'csv'")


# POINT CLOUD
def PointCloud(f, points, values):
    f.write('x, y, z, value\n')
    bar = tqdm(unit=' Points', desc='Writing', total=len(points))
    for i in range(len(points)):
        f.write('{0:.3f},'.format(points[i][0]))
        f.write('{0:.3f},'.format(points[i][1]))
        f.write('{0:.3f},'.format(points[i][2]))
        f.write('{0:.3f}\n'.format(values[i]))
        bar.update()
    bar.close()


# IP FLUENT
def IPFluent(f, meshtal, points, values):
    guion1 = '3'
    n_coord = meshtal.n_coordinates
    n_values = str(len(points))
    guion2 = '1'
    uds = 'uds-0'
    beginning = '{}\n{}\n{}\n{}\n{}\n'.format(guion1, n_coord, n_values, guion2, uds)

    f.write(beginning)
    f.write('(')

    bar_x = tqdm(unit=' x points', desc='Writing x', total=len(points))
    for i in range(len(points)):
        f.write('{0:.3f}\n'.format(points[i][0]))
        bar_x.update()
    bar_x.close()

    f.write(')\n')
    f.write('(')

    bar_y = tqdm(unit=' y points', desc='Writing y', total=len(points))
    for i in range(len(points)):
        f.write('{0:.3f}\n'.format(points[i][1]))
        bar_y.update()
    bar_y.close()

    f.write(')\n')
    f.write('(')

    bar_z = tqdm(unit=' z points', desc='Writing z', total=len(points))
    for i in range(len(points)):
        f.write('{0:.3f}\n'.format(points[i][2]))
        bar_z.update()
    bar_z.close()

    f.write(')\n')
    f.write('(')

    bar_val = tqdm(unit=' values', desc='Writing values', total=len(values))
    for i in range(len(points)):
        f.write('{0:.3f}\n'.format(values[i]))
        bar_val.update()
    bar_val.close()

    f.write(')\n')


# CSV
def CSV(f, meshtal, points, list_array_names):
    writer = csv.writer(f)

    bar = tqdm(unit=' Points', desc='Writing', total=len(points))
    for i in range(len(points)):
        csv_points = ['{0:.3f}'.format(points[i][0]),
                      ' {0:.3f}'.format(points[i][1]),
                      ' {0:.3f}'.format(points[i][2])]
        # multiply the values of the array/s selected by the safety factor
        for array_name in list_array_names:
            csv_points.append(' {0:.3f}'.format(meshtal.mesh[array_name][i] * safety_factor))

        writer.writerow(csv_points)
        bar.update()
    bar.close()

# END OF FUNCTION DEFINITIONS
