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
"""

# CODE: setup.py (module used to install vtkConverter)

# LANGUAGE: PYTHON 3.9

# AUTHOR/S: Xavier Mosquera

# e-MAIL/S: xavier.mosquera@estudiantat.upc.edu

# DATE: 31/01/2022

# Copyright F4E 2022

# IDM: F4E_D_2RCXX3 v1.0

from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="vtkConverter",
    version="1.1.0",
    description="Tool to analyze, modify and convert VTK files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Xavier Mosquera",
    keywords="MCNP, VTK, VTS, VTR",
    packages=["vtkconverter"],  # Required
    python_requires=">=3.6",
    install_requires=["numpy", "pyvista >= 0.32.1", "tqdm"],
    extras_require={"test": ["unittest"],},
)
