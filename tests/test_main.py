import unittest
import os
from vtkconverter import functions


class MyTestCase(unittest.TestCase):
    def test_example_csv(self):
        functions.open_mesh("tests/data/example.vts")
        functions.write_mesh("tests/data/example.vts", ["Values"], "csv")
        with open("tests/data/expected_results/example_['Values']_csv.csv", "r") as infile:
            expected = infile.read()
        with open("tests/data/example_['Values']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("tests/data/example_['Values']_csv.csv")
        self.assertEqual(expected, result)

    def test_vtk_cube_square_csv(self):
        functions.open_mesh("tests/data/test_VTK_CUBE_SQUARE.vtr")
        functions.write_mesh("tests/data/test_VTK_CUBE_SQUARE.vtr", ["Value - Total"], "csv")
        with open(
            "tests/data/expected_results/test_VTK_CUBE_SQUARE_['Value - Total']_csv.csv", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/test_VTK_CUBE_SQUARE_['Value - Total']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("tests/data/test_VTK_CUBE_SQUARE_['Value - Total']_csv.csv")
        self.assertEqual(expected, result)

    def test_meshtal_14_csv(self):
        functions.open_mesh("tests/data/meshtal_14.vts")
        functions.write_mesh("tests/data/meshtal_14.vts", ["Value - Total"], "csv")
        with open(
            "tests/data/expected_results/meshtal_14_['Value - Total']_csv.csv", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/meshtal_14_['Value - Total']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("tests/data/meshtal_14_['Value - Total']_csv.csv")
        self.assertEqual(expected, result)

    def test_cuvmsh_44_celf10_csv(self):
        functions.open_mesh("tests/data/cuvmsh_44_CuV_CELF10.vtr")
        functions.write_mesh("tests/data/cuvmsh_44_CuV_CELF10.vtr", ["Value - Total"], "csv")
        with open(
            "tests/data/expected_results/cuvmsh_44_CuV_CELF10_['Value - Total']_csv.csv", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/cuvmsh_44_CuV_CELF10_['Value - Total']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("tests/data/cuvmsh_44_CuV_CELF10_['Value - Total']_csv.csv")
        self.assertEqual(expected, result)

    def test_rhc_inboard_csv(self):
        functions.open_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk")
        functions.write_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk", ["NHD[W/cm3]"], "csv")
        with open(
            "tests/data/expected_results/PS_NHD_DIV_RHC_INBOARD_['NHD[W-cm3]']_csv.csv", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/PS_NHD_DIV_RHC_INBOARD_['NHD[W-cm3]']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("tests/data/PS_NHD_DIV_RHC_INBOARD_['NHD[W-cm3]']_csv.csv")
        self.assertEqual(expected, result)

    def test_rhc_inboard_ip_fluent(self):
        functions.open_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk")
        functions.write_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk", ["NHD[W/cm3]"], "ip_fluent")
        with open(
            "tests/data/expected_results/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_ip_fluent.txt", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_ip_fluent.txt", "r") as infile:
            result = infile.read()
        os.remove("tests/data/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_ip_fluent.txt")
        self.assertEqual(expected, result)

    def test_rhc_inboard_point_cloud(self):
        functions.open_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk")
        functions.write_mesh("tests/data/PS_NHD_DIV_RHC_INBOARD.vtk", ["NHD[W/cm3]"], "point_cloud")
        with open(
            "tests/data/expected_results/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_point_cloud.txt", "r"
        ) as infile:
            expected = infile.read()
        with open("tests/data/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_point_cloud.txt", "r") as infile:
            result = infile.read()
        os.remove("tests/data/PS_NHD_DIV_RHC_INBOARD_NHD[W-cm3]_point_cloud.txt")
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
