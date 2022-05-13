"""
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


##----------------------------------------------------------------------------##
##                         ********    **   ********                          ##
##                         ********   ***   ********                          ##
##                         **        ** *   **                                ##
##                         ******   ******  ******                            ##
##                         ******   ******  ******                            ##
##                         **          **   ***                               ##
##                         **          **   ********                          ##
##                         **          **   ********                          ##
##                                                                            ##
##----------------------------------------------------------------------------##
##                       TSS / A&C / Nuclear Section                          ##
##----------------------------------------------------------------------------##
##                                                                            ##
##                         Fusion for Energy                                  ##
##                         c/ Josep Pla, n2                                   ##
##                      Torres Diagonal Litoral B3                            ##
##                         Barcelona (Spain)                                  ##
##                          +34 93 320 1800                                   ##
##                    http://fusionforenergy.europa.eu/                       ##
##                                                                            ##
##----------------------------------------------------------------------------##

CODE: vtkConverter

LANGUAGE: PYTHON 3.6

AUTHOR/S: Xavier Mosquera

e-MAIL/S: xavier.mosquera@estudiantat.upc.edu

DATE: 31/01/2022

Copyright F4E 2022

IDM: F4E_D_2RCXX3 v1.0

DESCRIPTION: It converts the VTK format files produced by MESH2VTK into other suitable formats,
             such as Point Cloud, IP Fluent or CSV.The tool is a python 3.9 based script able to
             read any VTK, VTR or VTS produced by MESH2VTK.
             The mesh from the VTK, opened and operated through pyvista, is composed by several points
             and cells and contains information that corresponds to either point or cell. The tool
             incorporates also functions to display information of the meshes, operate
             with meshes (translate, rotate, joint), change scale and safety factor and export to VTK again.
             The tool is used through a text based interactive menu, and it can be run under Windows or Linus systems.


USAGE:      python -m vtkconverter

OUTPUT:     VTKfilename + Array name + Format + .txt/.csv

VERSIONS:
           1.0 [2022-01-31]  ---> Developed by Xavier Mosquera (UPC) under supervision of
                                  Marco Fabbri (F4E) & Alvaro Cubi (F4E-EXT).
                                  Starting version.


IMPROVEMENTS:
              -->
              -->
"""
import os
import tkinter
from tkinter import filedialog
from vtkconverter import functions

# Define shown menus
principal_menu = """
 ***************************
   Process  VTK Meshtally
 ***************************

 * Append VTK file            (open)
 * Display mesh information   (info)
 * Convert file               (write)
 * Mesh operation             (operate) 
 * Export file to vtk         (export)
 * Scale Factor               (scale)
 * Safety Factor              (safety)
 * Exit                       (end)
"""

info_menu = """
 ***************************
      Info of a file
 ***************************

 * Mesh info                  (mesh)
 * Array info                 (array)
 * Exit                       (end)
"""

write_menu = """
 ***************************
      Write a file
 ***************************
 * Output formats:
   - point_cloud             
   - ip_fluent            
   - csv                     
 * Exit                       (end)
"""

operation_menu = """
 ***************************
      Operate a file
 ***************************
     
 * Translate                  (translate)
 * Rotate                     (rotate)
 * Joint mesh                 (joint)
 * Exit                       (end)
"""

export_menu = """
 ***************************
      Export a file
 ***************************
 * Export formats:
   - binary
   - ascii
 * Exit                       (end)
"""

scale_menu = """
 ***************************
     Change scale factor
 ***************************
 
 * Exit                       (end)
"""

safety_menu = """
 ***************************
     Change safety factor
 ***************************

* Exit                       (end)
"""


# Define functions
def input_files():  # display files to select
    print("\n Input files :")
    list_of_files = list(functions.meshtals.keys())
    for i in range(len(list_of_files)):
        print(f" - [{i}] {list_of_files[i]}")


def input_arrays(filename):  # display arrays to select
    print("\n Array names :")
    list_arrays = (
        functions.meshtals[filename].cells_info
        + functions.meshtals[filename].points_info
    )
    for i in range(len(list_arrays)):
        print(f" - [{i}] {list_arrays[i]}")


def select_file():  # select a file by index
    list_of_files = list(functions.meshtals.keys())
    while True:
        index_file = input(" Select index file #:")
        try:
            index_file = int(index_file)  # verify the input is an integer

            if index_file < len(
                list_of_files
            ):  # if this is true, the index corresponds to one file of the list
                filename = list_of_files[index_file]
                break
            else:
                print(" Bad index number")
        except ValueError:
            print(" Error. Select an index number")
    return filename


def select_array(filename):  # select an array by index
    list_arrays = (
        functions.meshtals[filename].cells_info
        + functions.meshtals[filename].points_info
    )  # list of available arrays
    while True:
        index_array = input(" Select index array #:")
        try:
            index_array = int(index_array)  # verify the input is an integer
            if index_array < len(
                list_arrays
            ):  # if this is true, the index corresponds to one array of the list
                array = list_arrays[index_array]
                break
            else:
                print(" Bad index number")
        except ValueError:
            print(" Error. Select an index number")
    return array


def select_multi_array(filename):  # select one or more arrays by index
    list_arrays = (
        functions.meshtals[filename].cells_info
        + functions.meshtals[filename].points_info
    )
    while True:
        i = 0
        index_arrays = input(" Select index of arrays #:")
        list_of_index_arrays = index_arrays.split(",")
        list_of_arrays = []
        for index_array in list_of_index_arrays:
            try:
                index_array = int(index_array)  # verify the input is an integer

                if index_array < len(
                    list_arrays
                ):  # if this is true, the index corresponds to one array of the list
                    list_of_arrays.append(
                        list_arrays[index_array]
                    )  # The selected array is appended to the output list
                else:
                    print(f" Bad index number : {index_array}")
                    i += 1
            except ValueError:
                print(f" Error with: {index_array}. Select an index number")
                i += 1
        if i == 0:  # only if there are 0 errors or bad indexes out of range
            return list_of_arrays


def answer_loop(menu):  # each menu accepts some specific keys
    principal_keys = [
        "open",
        "info",
        "write",
        "operate",
        "export",
        "scale",
        "safety",
        "end",
    ]
    info_keys = ["mesh", "array", "end"]
    write_keys = ["point_cloud", "ip_fluent", "csv", "end"]
    operation_keys = ["translate", "rotate", "joint", "end"]
    export_keys = ["binary", "ascii", "end"]
    menu_list = {
        "principal": principal_keys,
        "info": info_keys,
        "write": write_keys,
        "operate": operation_keys,
        "export": export_keys,
    }
    while True:
        ans = input(" enter action :")

        if ans in menu_list[menu]:
            break
        else:
            print(" not expected keyword")
    return ans


# MENUS of the program
def open_file():
    root = tkinter.Tk()
    root.wm_withdraw()  # This completely hides the root window
    filename = filedialog.askopenfilename(
        filetypes=[("vtk files", ".vtk .vts .vtr .vtu")]
    )
    # filename = input(' Write file name :')  Delete 3 rows above and root.destroy() and
    # write this to input the file by writing its filename
    functions.open_mesh(filename)
    root.destroy()
    input_files()


def info():
    print(info_menu)
    ans = answer_loop("info")
    list_of_files = list(functions.meshtals.keys())
    if ans != "end":
        if len(list_of_files) > 1:
            input_files()
            filename = select_file()
        else:
            filename = list_of_files[0]
        if ans == "mesh":
            functions.print_general_info(filename)
        elif ans == "array":
            input_arrays(filename)
            array = select_array(filename)
            functions.print_array_info(filename, array)


def write():
    print(write_menu)
    ans = answer_loop("write")
    list_of_files = list(functions.meshtals.keys())
    if ans != "end":
        if len(list_of_files) > 1:
            input_files()
            filename = select_file()
        else:
            filename = list_of_files[0]
        input_arrays(filename)
        list_of_arrays = select_multi_array(filename)
        functions.write_mesh(filename, list_of_arrays, ans)


def operate():
    print(operation_menu)
    ans = answer_loop("operate")
    list_of_files = list(functions.meshtals.keys())
    filename = None
    if ans != "end":
        if len(list_of_files) > 1:
            input_files()
            filename = select_file()
        else:
            filename = list_of_files[0]

    if ans == "translate":
        ok = [True, True, True]
        x = None
        y = None
        z = None
        while ok != [False, False, False]:
            ok = [True, True, True]
            xyz = input(" Select translation in x,y,z :").split(",")
            if len(xyz) == 3:
                try:
                    x = float(xyz[0])
                    ok[0] = False
                except ValueError:
                    print("Wrong x value. Write a number")
                try:
                    y = float(xyz[1])
                    ok[1] = False
                except ValueError:
                    print("Wrong y value. Write a number")
                try:
                    z = float(xyz[2])
                    ok[2] = False
                except ValueError:
                    print("Wrong z value. Write a number")
            else:
                print(" Bad input. Write 3 numbers")
        functions.translate(filename, x, y, z)

    elif ans == "rotate":
        ok = [True, True, True]
        x = None
        y = None
        z = None
        while ok != [False, False, False]:
            ok = [True, True, True]
            xyz = input(" Select rotation around x,y,z :").split(",")
            if (
                len(xyz) == 3
            ):  # it only accepts inputs which the 3 values are separated by commas, no spaces
                try:
                    x = float(xyz[0])
                    ok[0] = False
                except ValueError:
                    print("Wrong x value. Write a number")
                try:
                    y = float(xyz[1])
                    ok[1] = False
                except ValueError:
                    print("Wrong y value. Write a number")
                try:
                    z = float(xyz[2])
                    ok[2] = False
                except ValueError:
                    print("Wrong z value. Write a number")
            else:
                print(" Bad input. Write 3 numbers")
        functions.rotate(filename, x, y, z)
    elif ans == "joint":
        input_files()
        filename2 = select_file()
        functions.joint_mesh(filename, filename2)


def export():
    print(export_menu)
    ans = answer_loop("export")
    list_of_files = list(functions.meshtals.keys())
    if ans != "end":
        if len(list_of_files) > 1:
            input_files()
            filename = select_file()
        else:
            filename = list_of_files[0]
        functions.export_mesh(filename, ans)


def scale():
    print(scale_menu)
    print(f" Current Value: {functions.scale_factor}")

    while True:
        ans = input(" New scale factor :")
        if ans == "end":
            break
        else:
            try:
                ans = float(ans)
                break
            except ValueError:
                print(" Bad new value. Write one number")
    if ans != "end":
        functions.change_scale_factor(ans)


def safety():
    print(safety_menu)
    print(f" Current Value: {functions.safety_factor}")
    while True:
        ans = input(" New safety factor :")
        if ans == "end":
            break
        else:
            try:
                ans = float(ans)
                break
            except ValueError:
                print(" Bad new value. Write one number")
    if ans != "end":
        functions.change_safety_factor(ans)


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main():
    # Screen
    clear_screen()
    print(principal_menu)
    ans = answer_loop("principal")
    while True:
        if ans == "open":
            open_file()
        elif ans == "info":
            if len(functions.meshtals.keys()) == 0:
                print(" No meshtally file")
            else:
                info()
        elif ans == "write":
            if len(functions.meshtals.keys()) == 0:
                print(" No meshtally file")
            else:
                write()
        elif ans == "operate":
            if len(functions.meshtals.keys()) == 0:
                print(" No meshtally file")
            else:
                operate()
        elif ans == "export":
            if len(functions.meshtals.keys()) == 0:
                print(" No meshtally file")
            else:
                export()
        elif ans == "scale":
            scale()
        elif ans == "safety":
            safety()
        else:
            break
        ans = answer_loop("principal")
        clear_screen()
        print(principal_menu)
