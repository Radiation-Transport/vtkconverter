import os
import unittest
from vtkconverter import functions
import numpy as np
from numpy.testing import assert_array_almost_equal

EXAMPLE_VTK_FILE = "data/example.vts"


class MyTestCase(unittest.TestCase):
    def test_meshtally(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        self.assertEqual("data/example.vts", mesh_tally.filename)
        self.assertEqual(8, mesh_tally.mesh.n_cells)
        self.mesh_tally = mesh_tally
        return

    def test_centers(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        expected = np.array(
            [
                [0.5, 0.5, 1.0],
                [1.5, 0.5, 1.0],
                [0.5, 1.5, 1.0],
                [1.5, 1.5, 1.0],
                [0.5, 0.5, 3.0],
                [1.5, 0.5, 3.0],
                [0.5, 1.5, 3.0],
                [1.5, 1.5, 3.0],
            ]
        )
        assert_array_almost_equal(expected, mesh_tally.centers)
        return

    def test_cell_info(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        self.assertListEqual(["Values"], mesh_tally.cells_info)
        return

    def test_get_array_type(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        self.assertEqual("cells", functions.get_array_type(mesh_tally, "Values"))
        return

    def test_integral_and_average(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        (
            integral_no_volume,
            average_no_volume,
            integral,
            average,
        ) = functions.integral_and_average("mesh_name", "Values")
        self.assertAlmostEqual(33, integral_no_volume)
        self.assertAlmostEqual(4.125, average_no_volume)
        self.assertAlmostEqual(66, integral)
        self.assertAlmostEqual(4.125, average)
        return

    def test_translate(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        functions.translate("mesh_name", x=1, y=2, z=3)
        new_centers = functions.meshtals["data/example+Trans(1,2,3).vts"].centers
        self.assertAlmostEqual(1.5, new_centers[0][0])
        self.assertAlmostEqual(2.5, new_centers[0][1])
        self.assertAlmostEqual(4, new_centers[0][2])
        return

    def test_rotate(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        functions.rotate("mesh_name", theta_z=180)
        new_centers = functions.meshtals["data/example+Rot(0,0,180).vts"].centers
        self.assertAlmostEqual(-0.5, new_centers[0][0])
        self.assertAlmostEqual(-0.5, new_centers[0][1])
        self.assertAlmostEqual(1, new_centers[0][2])
        return

    def test_write_mesh_point_cloud(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        functions.write_mesh("mesh_name", ["Values"], "point_cloud")
        with open(
            "data/expected_results/example_Values_point_cloud.txt", "r"
        ) as infile:
            expected = infile.read()
        with open("data/example_Values_point_cloud.txt", "r") as infile:
            result = infile.read()
        os.remove("data/example_Values_point_cloud.txt")
        self.assertEqual(expected, result)
        return

    def test_write_mesh_ip_fluent(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        functions.write_mesh("mesh_name", ["Values"], "ip_fluent")
        with open("data/expected_results/example_Values_ip_fluent.txt", "r") as infile:
            expected = infile.read()
        with open("data/example_Values_ip_fluent.txt", "r") as infile:
            result = infile.read()
        os.remove("data/example_Values_ip_fluent.txt")
        self.assertEqual(expected, result)
        return

    def test_write_mesh_csv(self):
        mesh_tally = functions.MeshTally(EXAMPLE_VTK_FILE)
        functions.meshtals = {"mesh_name": mesh_tally}
        functions.write_mesh("mesh_name", ["Values"], "csv")
        with open("data/expected_results/example_['Values']_csv.csv", "r") as infile:
            expected = infile.read()
        with open("data/example_['Values']_csv.csv", "r") as infile:
            result = infile.read()
        os.remove("data/example_['Values']_csv.csv")
        self.assertEqual(expected, result)
        return


if __name__ == "__main__":
    unittest.main()
