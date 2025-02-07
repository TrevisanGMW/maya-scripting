from unittest.mock import patch
from io import StringIO
import unittest
import logging
import sys
import os

# Logging Setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Import Utility and Maya Test Tools
test_utils_dir = os.path.dirname(__file__)
tests_dir = os.path.dirname(test_utils_dir)
package_root_dir = os.path.dirname(tests_dir)
for to_append in [package_root_dir, tests_dir]:
    if to_append not in sys.path:
        sys.path.append(to_append)
from gt.tests import maya_test_tools
from gt.core import transform as core_transform
cmds = maya_test_tools.cmds


class TestTransformCore(unittest.TestCase):
    def setUp(self):
        maya_test_tools.force_new_scene()
        self.vector_a = core_transform.Vector3(1, 2, 3)
        self.vector_b = core_transform.Vector3(4, 5, 6)

    @classmethod
    def setUpClass(cls):
        maya_test_tools.import_maya_standalone(initialize=True)  # Start Maya Headless (mayapy.exe)

    def assertAlmostEqualSigFig(self, arg1, arg2, tolerance=2):
        """
        Asserts that two numbers are almost equal up to a given number of significant figures.

        Args:
            self (object): The current test case or class object.
            arg1 (float): The first number for comparison.
            arg2 (float): The second number for comparison.
            tolerance (int, optional): The number of significant figures to consider for comparison. Default is 2.

        Returns:
            None

        Raises:
            AssertionError: If the significands of arg1 and arg2 differ by more than the specified tolerance.

        Example:
            obj = TestClass()
            obj.assertAlmostEqualSigFig(3.145, 3.14159, tolerance=3)
            # No assertion error will be raised as the first 3 significant figures are equal (3.14)
        """
        if tolerance > 1:
            tolerance = tolerance - 1

        str_formatter = '{0:.' + str(tolerance) + 'e}'
        significand_1 = float(str_formatter.format(arg1).split('e')[0])
        significand_2 = float(str_formatter.format(arg2).split('e')[0])

        exponent_1 = int(str_formatter.format(arg1).split('e')[1])
        exponent_2 = int(str_formatter.format(arg2).split('e')[1])

        self.assertEqual(significand_1, significand_2)
        self.assertEqual(exponent_1, exponent_2)

    # --------------------------------------------- Vector3 Start -------------------------------------------
    def test_vector3_class_as_string(self):
        vector3_object = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        expected = "(x=1.2, y=3.4, z=5.6)"
        result = str(vector3_object)
        self.assertEqual(expected, result)

    def test_vector3_class_as_list(self):
        vector3_object = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        result = [vector3_object.x, vector3_object.y, vector3_object.z]
        expected = [1.2, 3.4, 5.6]
        self.assertEqual(expected, result)

    def test_vector3_class_equality_true(self):
        vector3_object_a = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        vector3_object_b = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        result = vector3_object_a == vector3_object_b
        expected = True
        self.assertEqual(expected, result)

    def test_vector3_class_equality_false(self):
        vector3_object_a = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        vector3_object_b = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        result = vector3_object_a == vector3_object_b
        expected = True
        self.assertEqual(expected, result)

    def test_Vector3_init(self):
        vec = core_transform.Vector3()
        result = vec.get_as_tuple()
        expected = (0.0, 0.0, 0.0)
        self.assertEqual(expected, result)

        vec = core_transform.Vector3(x=1.0, y=2.0, z=3.0)
        result = vec.get_as_tuple()
        expected = (1.0, 2.0, 3.0)
        self.assertEqual(expected, result)

        vec = core_transform.Vector3(xyz=[4.0, 5.0, 6.0])
        expected = (4.0, 5.0, 6.0)
        result = vec.get_as_tuple()
        self.assertEqual(expected, result)

    def test_Vector3_invalid_input(self):
        with self.assertRaises(ValueError):
            core_transform.Vector3(x="not a number")

    def test_Vector3_eq(self):
        vec1 = core_transform.Vector3(1.0, 2.0, 3.0)
        vec2 = core_transform.Vector3(1.0, 2.0, 3.0)
        vec3 = core_transform.Vector3(4.0, 5.0, 6.0)
        expected = True
        result = vec1 == vec2
        self.assertEqual(expected, result)

        expected = False
        result = vec1 == vec3
        self.assertEqual(expected, result)

    def test_Vector3_add(self):
        vec1 = core_transform.Vector3(1.0, 2.0, 3.0)
        vec2 = core_transform.Vector3(4.0, 5.0, 6.0)
        expected = (5.0, 7.0, 9.0)
        added_vec = vec1 + vec2
        result = added_vec.get_as_tuple()
        self.assertEqual(expected, result)

    def test_Vector3_sub(self):
        vec1 = core_transform.Vector3(1.0, 2.0, 3.0)
        vec2 = core_transform.Vector3(4.0, 5.0, 6.0)
        expected = (3.0, 3.0, 3.0)
        result = (vec2 - vec1).get_as_tuple()
        self.assertEqual(expected, result)

    def test_Vector3_mul(self):
        vec = core_transform.Vector3(1.0, 2.0, 3.0)
        scalar = 2.0
        expected = (2.0, 4.0, 6.0)
        result = (vec * scalar).get_as_tuple()
        self.assertEqual(expected, result)

    def test_Vector3_magnitude(self):
        vec = core_transform.Vector3(3.0, 4.0, 0.0)
        expected = 5.0
        result = vec.magnitude()
        self.assertEqual(expected, result)

    def test_Vector3_dot(self):
        vec1 = core_transform.Vector3(1.0, 2.0, 3.0)
        vec2 = core_transform.Vector3(4.0, 5.0, 6.0)
        expected = 32.0
        result = vec1.dot(vec2)
        self.assertEqual(expected, result)

    def test_Vector3_cross(self):
        vec1 = core_transform.Vector3(1.0, 0.0, 0.0)
        vec2 = core_transform.Vector3(0.0, 1.0, 0.0)
        expected = (0.0, 0.0, 1.0)
        result = vec1.cross(vec2).get_as_tuple()
        self.assertEqual(expected, result)

    def test_Vector3_set_from_list(self):
        vec = core_transform.Vector3()
        vec.set_from_tuple((4.0, 5.0, 6.0))
        expected = (4.0, 5.0, 6.0)
        result = vec.get_as_tuple()
        self.assertEqual(expected, result)

        with self.assertRaises(ValueError):
            vec.set_from_tuple((1.0, 2.0, 3.0, 4.0))

    def test_Vector3_less_than(self):
        v1 = core_transform.Vector3(1, 2, 3)
        v2 = core_transform.Vector3(4, 5, 6)
        self.assertTrue(v1 < v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v1 < v1)

    def test_Vector3_less_than_or_equal(self):
        v1 = core_transform.Vector3(1, 2, 3)
        v2 = core_transform.Vector3(4, 5, 6)
        self.assertTrue(v1 <= v2)
        self.assertFalse(v2 <= v1)
        self.assertTrue(v1 <= v1)

    def test_Vector3_greater_than(self):
        v1 = core_transform.Vector3(1, 2, 3)
        v2 = core_transform.Vector3(4, 5, 6)
        self.assertFalse(v1 > v2)
        self.assertTrue(v2 > v1)
        self.assertFalse(v1 > v1)

    def test_Vector3_greater_than_or_equal(self):
        v1 = core_transform.Vector3(1, 2, 3)
        v2 = core_transform.Vector3(4, 5, 6)
        self.assertFalse(v1 >= v2)
        self.assertTrue(v2 >= v1)
        self.assertTrue(v1 >= v1)

    def test_Vector3_x_setter(self):
        vector = core_transform.Vector3(0, 0, 0)
        vector.set_x(x=10)
        expected = 10
        self.assertEqual(expected, vector.x)

    def test_Vector3_y_setter(self):
        vector = core_transform.Vector3(0, 0, 0)
        vector.set_y(y=10)
        expected = 10
        self.assertEqual(expected, vector.y)

    def test_Vector3_z_setter(self):
        vector = core_transform.Vector3(0, 0, 0)
        vector.set_z(z=10)
        expected = 10
        self.assertEqual(expected, vector.z)

    # --------------------------------------------------- Vector3 End -------------------------------------------------

    # ------------------------------------------------- Transform Start -----------------------------------------------
    def test_transform_class_as_string(self):
        vector3_object = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        transform_object = core_transform.Transform(position=vector3_object,
                                                    rotation=vector3_object,
                                                    scale=vector3_object)
        result = str(transform_object)
        expected = "position=(x=1.2, y=3.4, z=5.6), " \
                   "rotation=(x=1.2, y=3.4, z=5.6), " \
                   "scale=(x=1.2, y=3.4, z=5.6)"
        self.assertEqual(expected, result)

    def test_transform_class_position_as_list(self):
        vector3_object = core_transform.Vector3(x=1.2, y=3.4, z=5.6)
        transform_object = core_transform.Transform(position=vector3_object,
                                                    rotation=vector3_object,
                                                    scale=vector3_object)
        result = [transform_object.position.x, transform_object.position.y, transform_object.position.z]
        expected = [1.2, 3.4, 5.6]
        self.assertEqual(expected, result)

    def test_transform_class_rotation_as_list(self):
        vector3_object = core_transform.Vector3(x=30, y=-45, z=90)
        transform_object = core_transform.Transform(position=vector3_object,
                                                    rotation=vector3_object,
                                                    scale=vector3_object)
        result = [transform_object.rotation.x, transform_object.rotation.y, transform_object.rotation.z]
        expected = [30, -45, 90]
        self.assertEqual(expected, result)

    def test_transform_class_scale_as_list(self):
        vector3_object = core_transform.Vector3(x=1, y=2, z=3)
        transform_object = core_transform.Transform(position=vector3_object,
                                                    rotation=vector3_object,
                                                    scale=vector3_object)
        result = [transform_object.scale.x, transform_object.scale.y, transform_object.scale.z]
        expected = [1, 2, 3]
        self.assertEqual(expected, result)

    def test_transform_class_equality_one(self):
        vector3_object = core_transform.Vector3(x=1, y=2, z=3)
        transform_object_one = core_transform.Transform(position=vector3_object,
                                                        rotation=vector3_object,
                                                        scale=vector3_object)
        transform_object_two = core_transform.Transform(position=vector3_object,
                                                        rotation=vector3_object,
                                                        scale=vector3_object)
        result = transform_object_one == transform_object_two
        expected = True
        self.assertEqual(expected, result)

    def test_transform_class_equality_two(self):
        vector3_object_one = core_transform.Vector3(x=1, y=2, z=3)
        vector3_object_two = core_transform.Vector3(x=4, y=5, z=6)
        transform_object_one = core_transform.Transform(position=vector3_object_one,
                                                        rotation=vector3_object_one,
                                                        scale=vector3_object_one)
        transform_object_two = core_transform.Transform(position=vector3_object_two,
                                                        rotation=vector3_object_two,
                                                        scale=vector3_object_two)
        result = transform_object_one == transform_object_two
        expected = False
        self.assertEqual(expected, result)

    def test_transform_eq(self):
        transform_a = core_transform.Transform(self.vector_a, self.vector_a, self.vector_a)
        transform_b = core_transform.Transform(self.vector_b, self.vector_b, self.vector_b)

        expected = True
        result = transform_a == transform_a
        self.assertEqual(expected, result)

        expected = False
        result = transform_a == transform_b
        self.assertEqual(expected, result)

    def test_transform_set_translation_from_tuple(self):
        transform = core_transform.Transform()
        transform.set_translation_from_tuple((10, 20, 30))
        expected = core_transform.Vector3(10, 20, 30)
        self.assertEqual(expected, transform.position)

    def test_transform_set_rotation_from_tuple(self):
        transform = core_transform.Transform()
        transform.set_rotation_from_tuple((45, 90, 0))
        expected = core_transform.Vector3(45, 90, 0)
        self.assertEqual(expected, transform.rotation)

    def test_transform_set_scale_from_tuple(self):
        transform = core_transform.Transform()
        transform.set_scale_from_tuple((2, 2, 2))
        expected = core_transform.Vector3(2, 2, 2)
        self.assertEqual(expected, transform.scale)

    def test_transform_lt(self):
        transform_a = core_transform.Transform(self.vector_a, self.vector_a, self.vector_a)
        transform_b = core_transform.Transform(self.vector_b, self.vector_b, self.vector_b)
        self.assertTrue(transform_a < transform_b)
        self.assertFalse(transform_b < transform_a)
        self.assertFalse(transform_a < transform_a)

    def test_transform_le(self):
        transform_a = core_transform.Transform(self.vector_a, self.vector_a, self.vector_a)
        transform_b = core_transform.Transform(self.vector_b, self.vector_b, self.vector_b)
        self.assertTrue(transform_a <= transform_b)
        self.assertFalse(transform_b <= transform_a)
        self.assertTrue(transform_a <= transform_a)

    def test_transform_gt(self):
        transform_a = core_transform.Transform(self.vector_a, self.vector_a, self.vector_a)
        transform_b = core_transform.Transform(self.vector_b, self.vector_b, self.vector_b)
        self.assertFalse(transform_a > transform_b)
        self.assertTrue(transform_b > transform_a)
        self.assertFalse(transform_a > transform_a)

    def test_transform_ge(self):
        transform_a = core_transform.Transform(self.vector_a, self.vector_a, self.vector_a)
        transform_b = core_transform.Transform(self.vector_b, self.vector_b, self.vector_b)
        self.assertFalse(transform_a >= transform_b)
        self.assertTrue(transform_b >= transform_a)
        self.assertTrue(transform_a >= transform_a)

    def test_transform_set_position_xyz(self):
        transform = core_transform.Transform()
        new_position = core_transform.Vector3(1, 2, 3)
        transform.set_position(xyz=new_position)
        self.assertEqual(new_position, transform.position)

    def test_transform_set_rotation_xyz(self):
        transform = core_transform.Transform()
        new_rotation = core_transform.Vector3(45, 0, 90)
        transform.set_rotation(xyz=new_rotation)
        self.assertEqual(new_rotation, transform.rotation)

    def test_transform_set_scale_xyz(self):
        transform = core_transform.Transform()
        new_scale = core_transform.Vector3(2, 2, 2)
        transform.set_scale(xyz=new_scale)
        self.assertEqual(new_scale, transform.scale)

    def test_transform_set_position_arg(self):
        transform = core_transform.Transform()
        new_position = core_transform.Vector3(1, 2, 3)
        transform.set_position(1, 2, 3)
        self.assertEqual(new_position, transform.position)

    def test_transform_set_rotation_arg(self):
        transform = core_transform.Transform()
        new_rotation = core_transform.Vector3(45, 0, 90)
        transform.set_rotation(45, 0, 90)
        self.assertEqual(new_rotation, transform.rotation)

    def test_transform_set_scale_arg(self):
        transform = core_transform.Transform()
        new_scale = core_transform.Vector3(2, 2, 2)
        transform.set_scale(2, 2, 2)
        self.assertEqual(new_scale, transform.scale)

    def test_transform_set_position_fewer_channels(self):
        transform = core_transform.Transform()
        new_position = core_transform.Vector3(1, 2, 3)
        transform.set_position(xyz=new_position.get_as_tuple())
        transform.set_position(x=10)
        new_position.set_x(x=10)
        self.assertEqual(new_position, transform.position)
        transform.set_position(y=15)
        new_position.set_y(y=15)
        self.assertEqual(new_position, transform.position)
        transform.set_position(z=20)
        new_position.set_z(z=20)
        self.assertEqual(new_position, transform.position)
        transform.set_position(x=0, z=20)
        new_position.set_x(x=0)
        new_position.set_z(z=20)
        self.assertEqual(new_position, transform.position)
        transform.set_position(x=5, y=10)
        new_position.set_x(x=5)
        new_position.set_y(y=10)
        self.assertEqual(new_position.get_as_tuple(), transform.position.get_as_tuple())

    def test_transform_set_rotation_fewer_channels(self):
        transform = core_transform.Transform()
        new_rotation = core_transform.Vector3(1, 2, 3)
        transform.set_rotation(xyz=new_rotation.get_as_tuple())
        transform.set_rotation(x=10)
        new_rotation.set_x(x=10)
        self.assertEqual(new_rotation, transform.rotation)
        transform.set_rotation(y=15)
        new_rotation.set_y(y=15)
        self.assertEqual(new_rotation, transform.rotation)
        transform.set_rotation(z=20)
        new_rotation.set_z(z=20)
        self.assertEqual(new_rotation, transform.rotation)
        transform.set_rotation(x=0, z=20)
        new_rotation.set_x(x=0)
        new_rotation.set_z(z=20)
        self.assertEqual(new_rotation, transform.rotation)
        transform.set_rotation(x=5, y=10)
        new_rotation.set_x(x=5)
        new_rotation.set_y(y=10)
        self.assertEqual(new_rotation.get_as_tuple(), transform.rotation.get_as_tuple())

    def test_transform_set_scale_fewer_channels(self):
        transform = core_transform.Transform()
        new_scale = core_transform.Vector3(1, 2, 3)
        transform.set_scale(xyz=new_scale.get_as_tuple())
        transform.set_scale(x=10)
        new_scale.set_x(x=10)
        self.assertEqual(new_scale, transform.scale)
        transform.set_scale(y=15)
        new_scale.set_y(y=15)
        self.assertEqual(new_scale, transform.scale)
        transform.set_scale(z=20)
        new_scale.set_z(z=20)
        self.assertEqual(new_scale, transform.scale)
        transform.set_scale(x=0, z=20)
        new_scale.set_x(x=0)
        new_scale.set_z(z=20)
        self.assertEqual(new_scale, transform.scale)
        transform.set_scale(x=5, y=10)
        new_scale.set_x(x=5)
        new_scale.set_y(y=10)
        self.assertEqual(new_scale.get_as_tuple(), transform.scale.get_as_tuple())

    def test_transform_set_trs_invalid_input(self):
        transform = core_transform.Transform()

        invalid_input = "not_a_vector"
        with self.assertLogs(level='WARNING'):
            transform.set_position(invalid_input)
            transform.set_rotation(invalid_input)
            transform.set_scale(invalid_input)

        self.assertEqual(core_transform.Vector3(0, 0, 0), transform.position)
        self.assertEqual(core_transform.Vector3(0, 0, 0), transform.rotation)
        self.assertEqual(core_transform.Vector3(1, 1, 1), transform.scale)

    def test_transform_set_position_tuple(self):
        transform = core_transform.Transform()
        new_position = (1, 2, 3)
        new_position_vector3 = core_transform.Vector3(*new_position)
        transform.set_position(xyz=new_position)
        self.assertEqual(new_position_vector3, transform.position)

    def test_transform_set_rotation_tuple(self):
        transform = core_transform.Transform()
        new_rotation = (45, 0, 90)
        new_rotation_vector3 = core_transform.Vector3(*new_rotation)
        transform.set_rotation(xyz=new_rotation)
        self.assertEqual(new_rotation_vector3, transform.rotation)

    def test_transform_set_scale_tuple(self):
        transform = core_transform.Transform()
        new_scale = (2, 2, 2)
        new_scale_vector3 = core_transform.Vector3(*new_scale)
        transform.set_scale(xyz=new_scale)
        self.assertEqual(new_scale_vector3, transform.scale)

    def test_set_transform_from_object(self):
        cube = maya_test_tools.create_poly_cube()
        cmds.setAttr(f'{cube}.ty', 5)
        cmds.setAttr(f'{cube}.ry', 35)
        cmds.setAttr(f'{cube}.sy', 2)
        transform = core_transform.Transform()
        transform.set_transform_from_object(obj_name=cube)
        expected_position = core_transform.Vector3(0, 5, 0)
        self.assertEqual(expected_position, transform.position)
        expected_rotate = core_transform.Vector3(0, 35, 0)
        self.assertEqual(expected_rotate, transform.rotation)
        expected_scale = core_transform.Vector3(1, 2, 1)
        self.assertEqual(expected_scale, transform.scale)

    def test_get_position(self):
        transform = core_transform.Transform()
        new_pos = (2, 2, 2)
        new_pos_vector3 = core_transform.Vector3(*new_pos)
        transform.set_position(xyz=new_pos_vector3)
        self.assertEqual(new_pos_vector3, transform.get_position())
        self.assertEqual(new_pos_vector3.get_as_tuple(), transform.get_position(as_tuple=True))

    def test_get_rotation(self):
        transform = core_transform.Transform()
        new_rot = (2, 2, 2)
        new_rot_vector3 = core_transform.Vector3(*new_rot)
        transform.set_rotation(xyz=new_rot_vector3)
        self.assertEqual(new_rot_vector3, transform.get_rotation())
        self.assertEqual(new_rot_vector3.get_as_tuple(), transform.get_rotation(as_tuple=True))

    def test_get_scale(self):
        transform = core_transform.Transform()
        new_sca = (2, 2, 2)
        new_sca_vector3 = core_transform.Vector3(*new_sca)
        transform.set_scale(xyz=new_sca_vector3)
        self.assertEqual(new_sca_vector3, transform.get_scale())
        self.assertEqual(new_sca_vector3.get_as_tuple(), transform.get_scale(as_tuple=True))

    def test_get_transform_as_dict(self):
        transform = core_transform.Transform()
        new_pos = (1, 1, 1)
        new_pos_vector3 = core_transform.Vector3(*new_pos)
        transform.set_position(xyz=new_pos_vector3)
        new_rot = (2, 2, 2)
        new_rot_vector3 = core_transform.Vector3(*new_rot)
        transform.set_rotation(xyz=new_rot_vector3)
        new_sca = (3, 3, 3)
        new_sca_vector3 = core_transform.Vector3(*new_sca)
        transform.set_scale(xyz=new_sca_vector3)
        result = transform.get_transform_as_dict()
        expected = {"position": new_pos,
                    "rotation": new_rot,
                    "scale": new_sca,
                    }
        self.assertEqual(expected, result)

    def test_set_transform_from_dict(self):
        transform = core_transform.Transform()
        new_pos = (1, 1, 1)
        new_rot = (2, 2, 2)
        new_sca = (3, 3, 3)
        expected = {"position": new_pos,
                    "rotation": new_rot,
                    "scale": new_sca,
                    }
        transform.set_transform_from_dict(transform_dict=expected)
        result = transform.get_transform_as_dict()
        self.assertEqual(expected, result)

    # -------------------------------------------------- Transform End ------------------------------------------------

    def test_move_to_origin(self):
        cube = maya_test_tools.create_poly_cube()
        cmds.setAttr(f"{cube}.tx", 5)
        cmds.setAttr(f"{cube}.ty", 5)
        cmds.setAttr(f"{cube}.tz", 5)
        core_transform.move_to_origin(cube)
        expected = 0
        result_x = cmds.getAttr(f"{cube}.tx")
        result_y = cmds.getAttr(f"{cube}.ty")
        result_z = cmds.getAttr(f"{cube}.tz")
        self.assertEqual(expected, result_x)
        self.assertEqual(expected, result_y)
        self.assertEqual(expected, result_z)

    @patch('sys.stdout', new_callable=StringIO)
    def test_move_selection_to_origin(self, mocked_stdout):
        cube = maya_test_tools.create_poly_cube()
        cmds.setAttr(f"{cube}.tx", 5)
        cmds.setAttr(f"{cube}.ty", 5)
        cmds.setAttr(f"{cube}.tz", 5)
        cmds.select(cube)
        core_transform.move_selection_to_origin()
        expected = 0
        result_x = cmds.getAttr(f"{cube}.tx")
        result_y = cmds.getAttr(f"{cube}.ty")
        result_z = cmds.getAttr(f"{cube}.tz")
        self.assertEqual(expected, result_x)
        self.assertEqual(expected, result_y)
        self.assertEqual(expected, result_z)
        printed_value = mocked_stdout.getvalue()
        expected = '"pCube1" was moved to the origin\n'
        self.assertEqual(expected, printed_value)

    def test_overwrite_xyz_values(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions=None)
        expected = [1, 2, 3]
        self.assertEqual(expected, result)

    def test_overwrite_xyz_values_overwrite_x(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions="x")
        expected = [4, 2, 3]
        self.assertEqual(expected, result)

    def test_overwrite_xyz_values_overwrite_y(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions="y")
        expected = [1, 5, 3]
        self.assertEqual(expected, result)

    def test_overwrite_xyz_values_overwrite_z(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions="z")
        expected = [1, 2, 6]
        self.assertEqual(expected, result)

    def test_overwrite_xyz_values_overwrite_xyz(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions="xyz")
        expected = [4, 5, 6]
        self.assertEqual(expected, result)

    def test_overwrite_xyz_values_overwrite_xyz_tuple(self):

        result = core_transform.overwrite_xyz_values(passthrough_xyz=[1, 2, 3],
                                                     overwrite_xyz=[4, 5, 6],
                                                     overwrite_dimensions=('x', 'y', 'z'))
        expected = [4, 5, 6]
        self.assertEqual(expected, result)

    def test_match_translate(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets)
        expected = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected, result_x)
            self.assertEqual(expected, result_y)
            self.assertEqual(expected, result_z)

    def test_match_translate_skip_x(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets, skip="x")
        expected_x = 0
        expected_y = 5
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_translate_skip_y(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets, skip="y")
        expected_x = 5
        expected_y = 0
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_translate_skip_z(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets, skip="z")
        expected_x = 5
        expected_y = 5
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_translate_skip_xyz(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets, skip="xyz")
        expected_x = 0
        expected_y = 0
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_translate_skip_xyz_tuple(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.tx", 5)
        cmds.setAttr(f"{cube_source}.ty", 5)
        cmds.setAttr(f"{cube_source}.tz", 5)
        core_transform.match_translate(source=cube_source, target_list=targets, skip=("x", "y", "z"))
        expected_x = 0
        expected_y = 0
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_rotate(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets)
        expected = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected, result_x)
            self.assertAlmostEqualSigFig(expected, result_y)
            self.assertAlmostEqualSigFig(expected, result_z)

    def test_match_rotate_skip_x(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets, skip="x")
        expected_x = 0
        expected_y = 5
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_rotate_skip_y(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets, skip="y")
        expected_x = 5
        expected_y = 0
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_rotate_skip_z(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets, skip="z")
        expected_x = 5
        expected_y = 5
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_rotate_skip_xyz(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets, skip="xyz")
        expected_x = 0
        expected_y = 0
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_rotate_skip_xyz_tuple(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.rx", 5)
        cmds.setAttr(f"{cube_source}.ry", 5)
        cmds.setAttr(f"{cube_source}.rz", 5)
        core_transform.match_rotate(source=cube_source, target_list=targets, skip=("x", "y", "z"))
        expected_x = 0
        expected_y = 0
        expected_z = 0
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_scale(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets)
        expected = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected, result_x)
            self.assertEqual(expected, result_y)
            self.assertEqual(expected, result_z)

    def test_match_scale_skip_x(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets, skip="x")
        expected_x = 1
        expected_y = 5
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_scale_skip_y(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets, skip="y")
        expected_x = 5
        expected_y = 1
        expected_z = 5
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_scale_skip_z(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets, skip="z")
        expected_x = 5
        expected_y = 5
        expected_z = 1
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_scale_skip_xyz(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets, skip="xyz")
        expected_x = 1
        expected_y = 1
        expected_z = 1
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_scale_skip_xyz_tuple(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]
        cmds.setAttr(f"{cube_source}.sx", 5)
        cmds.setAttr(f"{cube_source}.sy", 5)
        cmds.setAttr(f"{cube_source}.sz", 5)
        core_transform.match_scale(source=cube_source, target_list=targets, skip=('x', 'y', 'z'))
        expected_x = 1
        expected_y = 1
        expected_z = 1
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)

    def test_match_transform(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]

        cmds.setAttr(f"{cube_source}.tx", 1)
        cmds.setAttr(f"{cube_source}.ty", 2)
        cmds.setAttr(f"{cube_source}.tz", 3)

        cmds.setAttr(f"{cube_source}.rx", 1)
        cmds.setAttr(f"{cube_source}.ry", 2)
        cmds.setAttr(f"{cube_source}.rz", 3)

        cmds.setAttr(f"{cube_source}.sx", 1)
        cmds.setAttr(f"{cube_source}.sy", 2)
        cmds.setAttr(f"{cube_source}.sz", 3)

        core_transform.match_transform(source=cube_source, target_list=targets)

        expected_x = 1
        expected_y = 2
        expected_z = 3
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)

    def test_match_transform_skip_xy(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]

        cmds.setAttr(f"{cube_source}.tx", 1)
        cmds.setAttr(f"{cube_source}.ty", 2)
        cmds.setAttr(f"{cube_source}.tz", 3)

        cmds.setAttr(f"{cube_source}.rx", 1)
        cmds.setAttr(f"{cube_source}.ry", 2)
        cmds.setAttr(f"{cube_source}.rz", 3)

        cmds.setAttr(f"{cube_source}.sx", 1)
        cmds.setAttr(f"{cube_source}.sy", 2)
        cmds.setAttr(f"{cube_source}.sz", 3)

        core_transform.match_transform(source=cube_source, target_list=targets,
                                       skip_translate="xy", skip_rotate="xy", skip_scale="xy")

        expected_x = 0
        expected_y = 0
        expected_z = 3

        expected_sca_x = 1
        expected_sca_y = 1
        expected_sca_z = 3

        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_x, result_x)
            self.assertEqual(expected_y, result_y)
            self.assertEqual(expected_z, result_z)
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_x, result_x)
            self.assertAlmostEqualSigFig(expected_y, result_y)
            self.assertAlmostEqualSigFig(expected_z, result_z)
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertAlmostEqualSigFig(expected_sca_x, result_x)
            self.assertAlmostEqualSigFig(expected_sca_y, result_y)
            self.assertAlmostEqualSigFig(expected_sca_z, result_z)

    def test_match_transform_skip_translate(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]

        cmds.setAttr(f"{cube_source}.tx", 1)
        cmds.setAttr(f"{cube_source}.ty", 2)
        cmds.setAttr(f"{cube_source}.tz", 3)

        cmds.setAttr(f"{cube_source}.rx", 1)
        cmds.setAttr(f"{cube_source}.ry", 2)
        cmds.setAttr(f"{cube_source}.rz", 3)

        cmds.setAttr(f"{cube_source}.sx", 1)
        cmds.setAttr(f"{cube_source}.sy", 2)
        cmds.setAttr(f"{cube_source}.sz", 3)

        core_transform.match_transform(source=cube_source, target_list=targets, translate=False)

        expected_pos_x = 0
        expected_pos_y = 0
        expected_pos_z = 0

        expected_rot_x = 1
        expected_rot_y = 2
        expected_rot_z = 3

        expected_sca_x = 1
        expected_sca_y = 2
        expected_sca_z = 3
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_pos_x, result_x)
            self.assertEqual(expected_pos_y, result_y)
            self.assertEqual(expected_pos_z, result_z)
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_rot_x, result_x)
            self.assertAlmostEqualSigFig(expected_rot_y, result_y)
            self.assertAlmostEqualSigFig(expected_rot_z, result_z)
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertAlmostEqualSigFig(expected_sca_x, result_x)
            self.assertAlmostEqualSigFig(expected_sca_y, result_y)
            self.assertAlmostEqualSigFig(expected_sca_z, result_z)

    def test_match_transform_skip_rotate(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]

        cmds.setAttr(f"{cube_source}.tx", 1)
        cmds.setAttr(f"{cube_source}.ty", 2)
        cmds.setAttr(f"{cube_source}.tz", 3)

        cmds.setAttr(f"{cube_source}.rx", 1)
        cmds.setAttr(f"{cube_source}.ry", 2)
        cmds.setAttr(f"{cube_source}.rz", 3)

        cmds.setAttr(f"{cube_source}.sx", 1)
        cmds.setAttr(f"{cube_source}.sy", 2)
        cmds.setAttr(f"{cube_source}.sz", 3)

        core_transform.match_transform(source=cube_source, target_list=targets, rotate=False)

        expected_pos_x = 1
        expected_pos_y = 2
        expected_pos_z = 3

        expected_rot_x = 0
        expected_rot_y = 0
        expected_rot_z = 0

        expected_sca_x = 1
        expected_sca_y = 2
        expected_sca_z = 3
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_pos_x, result_x)
            self.assertEqual(expected_pos_y, result_y)
            self.assertEqual(expected_pos_z, result_z)
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_rot_x, result_x)
            self.assertAlmostEqualSigFig(expected_rot_y, result_y)
            self.assertAlmostEqualSigFig(expected_rot_z, result_z)
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertAlmostEqualSigFig(expected_sca_x, result_x)
            self.assertAlmostEqualSigFig(expected_sca_y, result_y)
            self.assertAlmostEqualSigFig(expected_sca_z, result_z)

    def test_match_transform_skip_scale(self):
        cube_source = maya_test_tools.create_poly_cube()
        cube_target_one = maya_test_tools.create_poly_cube()
        cube_target_two = maya_test_tools.create_poly_cube()
        targets = [cube_target_one, cube_target_two]

        cmds.setAttr(f"{cube_source}.tx", 1)
        cmds.setAttr(f"{cube_source}.ty", 2)
        cmds.setAttr(f"{cube_source}.tz", 3)

        cmds.setAttr(f"{cube_source}.rx", 1)
        cmds.setAttr(f"{cube_source}.ry", 2)
        cmds.setAttr(f"{cube_source}.rz", 3)

        cmds.setAttr(f"{cube_source}.sx", 1)
        cmds.setAttr(f"{cube_source}.sy", 2)
        cmds.setAttr(f"{cube_source}.sz", 3)

        core_transform.match_transform(source=cube_source, target_list=targets, scale=False)

        expected_pos_x = 1
        expected_pos_y = 2
        expected_pos_z = 3

        expected_rot_x = 1
        expected_rot_y = 2
        expected_rot_z = 3

        expected_sca_x = 1
        expected_sca_y = 1
        expected_sca_z = 1
        for cube in targets:
            result_x = cmds.getAttr(f"{cube}.tx")
            result_y = cmds.getAttr(f"{cube}.ty")
            result_z = cmds.getAttr(f"{cube}.tz")
            self.assertEqual(expected_pos_x, result_x)
            self.assertEqual(expected_pos_y, result_y)
            self.assertEqual(expected_pos_z, result_z)
            result_x = cmds.getAttr(f"{cube}.rx")
            result_y = cmds.getAttr(f"{cube}.ry")
            result_z = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(expected_rot_x, result_x)
            self.assertAlmostEqualSigFig(expected_rot_y, result_y)
            self.assertAlmostEqualSigFig(expected_rot_z, result_z)
            result_x = cmds.getAttr(f"{cube}.sx")
            result_y = cmds.getAttr(f"{cube}.sy")
            result_z = cmds.getAttr(f"{cube}.sz")
            self.assertAlmostEqualSigFig(expected_sca_x, result_x)
            self.assertAlmostEqualSigFig(expected_sca_y, result_y)
            self.assertAlmostEqualSigFig(expected_sca_z, result_z)

    def test_set_equidistant_transforms(self):
        cube_start = maya_test_tools.create_poly_cube()
        cube_end = maya_test_tools.create_poly_cube()

        cube_one = maya_test_tools.create_poly_cube()
        cube_two = maya_test_tools.create_poly_cube()
        cube_three = maya_test_tools.create_poly_cube()

        targets = [cube_one, cube_two, cube_three]

        cmds.setAttr(f"{cube_end}.ty", 10)
        cmds.setAttr(f"{cube_end}.tz", 10)
        cmds.setAttr(f"{cube_end}.rx", 90)

        core_transform.set_equidistant_transforms(start=cube_start,
                                                  end=cube_end,
                                                  target_list=targets,
                                                  skip_start_end=True,
                                                  constraint='parent')

        expected_values = {cube_one: [0, 2.5, 2.5,
                                      21.59, 0, 0],
                           cube_two: [0, 5, 5,
                                      45, 0, 0],
                           cube_three: [0, 7.5, 7.5,
                                        68.4, 0, 0]}
        for cube, expected in expected_values.items():
            tx = cmds.getAttr(f"{cube}.tx")
            ty = cmds.getAttr(f"{cube}.ty")
            tz = cmds.getAttr(f"{cube}.tz")
            rx = cmds.getAttr(f"{cube}.rx")
            ry = cmds.getAttr(f"{cube}.ry")
            rz = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(tx, expected[0])
            self.assertAlmostEqualSigFig(ty, expected[1])
            self.assertAlmostEqualSigFig(tz, expected[2])
            self.assertAlmostEqualSigFig(rx, expected[3])
            self.assertAlmostEqualSigFig(ry, expected[4])
            self.assertAlmostEqualSigFig(rz, expected[5])

    def test_set_equidistant_transforms_skip_start_end(self):
        cube_start = maya_test_tools.create_poly_cube()
        cube_end = maya_test_tools.create_poly_cube()

        cube_one = maya_test_tools.create_poly_cube()
        cube_two = maya_test_tools.create_poly_cube()
        cube_three = maya_test_tools.create_poly_cube()

        targets = [cube_one, cube_two, cube_three]

        cmds.setAttr(f"{cube_end}.ty", 10)
        cmds.setAttr(f"{cube_end}.tz", 10)
        cmds.setAttr(f"{cube_end}.rx", 90)

        core_transform.set_equidistant_transforms(start=cube_start,
                                                  end=cube_end,
                                                  target_list=targets,
                                                  skip_start_end=False,
                                                  constraint='parent')

        expected_values = {cube_one: [0, 0, 0,
                                      0, 0, 0],
                           cube_two: [0, 5, 5,
                                      45, 0, 0],
                           cube_three: [0, 10, 10,
                                        90, 0, 0]}
        for cube, expected in expected_values.items():
            tx = cmds.getAttr(f"{cube}.tx")
            ty = cmds.getAttr(f"{cube}.ty")
            tz = cmds.getAttr(f"{cube}.tz")
            rx = cmds.getAttr(f"{cube}.rx")
            ry = cmds.getAttr(f"{cube}.ry")
            rz = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(tx, expected[0])
            self.assertAlmostEqualSigFig(ty, expected[1])
            self.assertAlmostEqualSigFig(tz, expected[2])
            self.assertAlmostEqualSigFig(rx, expected[3])
            self.assertAlmostEqualSigFig(ry, expected[4])
            self.assertAlmostEqualSigFig(rz, expected[5])

    def test_set_equidistant_transforms_point_type(self):
        cube_start = maya_test_tools.create_poly_cube()
        cube_end = maya_test_tools.create_poly_cube()

        cube_one = maya_test_tools.create_poly_cube()
        cube_two = maya_test_tools.create_poly_cube()
        cube_three = maya_test_tools.create_poly_cube()

        targets = [cube_one, cube_two, cube_three]

        cmds.setAttr(f"{cube_end}.ty", 10)
        cmds.setAttr(f"{cube_end}.tz", 10)
        cmds.setAttr(f"{cube_end}.rx", 90)

        core_transform.set_equidistant_transforms(start=cube_start,
                                                  end=cube_end,
                                                  target_list=targets,
                                                  skip_start_end=False,
                                                  constraint='point')

        expected_values = {cube_one: [0, 0, 0,
                                      0, 0, 0],
                           cube_two: [0, 5, 5,
                                      0, 0, 0],
                           cube_three: [0, 10, 10,
                                        0, 0, 0]}
        for cube, expected in expected_values.items():
            tx = cmds.getAttr(f"{cube}.tx")
            ty = cmds.getAttr(f"{cube}.ty")
            tz = cmds.getAttr(f"{cube}.tz")
            rx = cmds.getAttr(f"{cube}.rx")
            ry = cmds.getAttr(f"{cube}.ry")
            rz = cmds.getAttr(f"{cube}.rz")
            self.assertAlmostEqualSigFig(tx, expected[0])
            self.assertAlmostEqualSigFig(ty, expected[1])
            self.assertAlmostEqualSigFig(tz, expected[2])
            self.assertAlmostEqualSigFig(rx, expected[3])
            self.assertAlmostEqualSigFig(ry, expected[4])
            self.assertAlmostEqualSigFig(rz, expected[5])

    def test_translate_shapes(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.translate_shapes(obj_transform=crv, offset=(1, 0, 0))

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[1.0, 0.0, 1.0], [1.0, 0.0, 0.667], [1.0, 0.0, 0.0],
                    [1.0, 0.0, -1.0], [1.0, 0.0, -1.667], [1.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

    def test_rotate_shapes(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.rotate_shapes(obj_transform=crv, offset=(90, 0, 0), pivot=None)

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, -1.0, 0.0], [0.0, -0.667, 0.0], [0.0, 0.0, 0.0],
                    [0.0, 1.0, 0.0], [0.0, 1.667, 0.0], [0.0, 2.0, 0.0]]
        self.assertEqual(expected, cv_positions)

    def test_rotate_shapes_pivot(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.rotate_shapes(obj_transform=crv, offset=(0, 90, 0), pivot=(5, 0, 0))

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[6.0, 0.0, 5.0], [5.667, 0.0, 5.0], [5.0, 0.0, 5.0],
                    [4.0, 0.0, 5.0], [3.333, 0.0, 5.0], [3.0, 0.0, 5.0]]
        self.assertEqual(expected, cv_positions)

    def test_scale_shapes_integer(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.scale_shapes(obj_transform=crv, offset=2, pivot=None)

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 2.0], [0.0, 0.0, 1.334], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -2.0], [0.0, 0.0, -3.334], [0.0, 0.0, -4.0]]
        self.assertEqual(expected, cv_positions)

    def test_scale_shapes_tuple(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.scale_shapes(obj_transform=crv, offset=(2, 1, 1), pivot=None)

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

    def test_scale_shapes_pivot(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')

        num_cvs = cmds.getAttr(f"{crv}.spans")
        num_cvs += cmds.getAttr(f"{crv}.degree")
        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

        core_transform.scale_shapes(obj_transform=crv, offset=(2, 1, 1), pivot=(1, 2, 1))

        cv_positions = []
        for i in range(num_cvs):
            cv_position = cmds.pointPosition(f"{crv}.cv[{i}]", world=True)
            cv_positions.append(cv_position)

        expected = [[-1.0, 0.0, 1.0], [-1.0, 0.0, 0.667], [-1.0, 0.0, 0.0],
                    [-1.0, 0.0, -1.0], [-1.0, 0.0, -1.667], [-1.0, 0.0, -2.0]]
        self.assertEqual(expected, cv_positions)

    def test_get_component_positions_as_dict_world_space(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')
        cmds.move(0, 1, 0, crv)
        result = core_transform.get_component_positions_as_dict(obj_transform=crv,
                                                                full_path=True,
                                                                world_space=True)

        expected = {'|mocked_curve.cv[0]': [0.0, 1.0, 1.0],
                    '|mocked_curve.cv[1]': [0.0, 1.0, 0.667],
                    '|mocked_curve.cv[2]': [0.0, 1.0, 0.0],
                    '|mocked_curve.cv[3]': [0.0, 1.0, -1.0],
                    '|mocked_curve.cv[4]': [0.0, 1.0, -1.667],
                    '|mocked_curve.cv[5]': [0.0, 1.0, -2.0]}
        self.assertEqual(expected, result)

        result = core_transform.get_component_positions_as_dict(obj_transform=crv,
                                                                full_path=False,
                                                                world_space=True)

        expected = {'mocked_curve.cv[0]': [0.0, 1.0, 1.0],
                    'mocked_curve.cv[1]': [0.0, 1.0, 0.667],
                    'mocked_curve.cv[2]': [0.0, 1.0, 0.0],
                    'mocked_curve.cv[3]': [0.0, 1.0, -1.0],
                    'mocked_curve.cv[4]': [0.0, 1.0, -1.667],
                    'mocked_curve.cv[5]': [0.0, 1.0, -2.0]}
        self.assertEqual(expected, result)

    def test_get_component_positions_as_dict_object_space(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')
        cmds.move(0, 1, 0, crv)
        result = core_transform.get_component_positions_as_dict(obj_transform=crv,
                                                                full_path=True,
                                                                world_space=False) # False = Object Space

        expected = {'|mocked_curve.cv[0]': [0.0, 0.0, 1.0],
                    '|mocked_curve.cv[1]': [0.0, 0.0, 0.667],
                    '|mocked_curve.cv[2]': [0.0, 0.0, 0.0],
                    '|mocked_curve.cv[3]': [0.0, 0.0, -1.0],
                    '|mocked_curve.cv[4]': [0.0, 0.0, -1.667],
                    '|mocked_curve.cv[5]': [0.0, 0.0, -2.0]}
        self.assertEqual(expected, result)

        result = core_transform.get_component_positions_as_dict(obj_transform=crv,
                                                                full_path=False,
                                                                world_space=False)  # False = Object Space

        expected = {'mocked_curve.cv[0]': [0.0, 0.0, 1.0],
                    'mocked_curve.cv[1]': [0.0, 0.0, 0.667],
                    'mocked_curve.cv[2]': [0.0, 0.0, 0.0],
                    'mocked_curve.cv[3]': [0.0, 0.0, -1.0],
                    'mocked_curve.cv[4]': [0.0, 0.0, -1.667],
                    'mocked_curve.cv[5]': [0.0, 0.0, -2.0]}
        self.assertEqual(expected, result)

    def test_get_component_positions_as_dict_cube(self):
        cube = maya_test_tools.create_poly_cube(name="mocked_cube")
        cmds.move(0, 1, 0, cube)
        result = core_transform.get_component_positions_as_dict(obj_transform=cube,
                                                                full_path=True,
                                                                world_space=True)

        expected = {'|mocked_cube.vtx[0]': [-0.5, 0.5, 0.5],
                    '|mocked_cube.vtx[1]': [0.5, 0.5, 0.5],
                    '|mocked_cube.vtx[2]': [-0.5, 1.5, 0.5],
                    '|mocked_cube.vtx[3]': [0.5, 1.5, 0.5],
                    '|mocked_cube.vtx[4]': [-0.5, 1.5, -0.5],
                    '|mocked_cube.vtx[5]': [0.5, 1.5, -0.5],
                    '|mocked_cube.vtx[6]': [-0.5, 0.5, -0.5],
                    '|mocked_cube.vtx[7]': [0.5, 0.5, -0.5]}
        self.assertEqual(expected, result)

        result = core_transform.get_component_positions_as_dict(obj_transform=cube,
                                                                full_path=False,
                                                                world_space=True)

        expected = {'mocked_cube.vtx[0]': [-0.5, 0.5, 0.5],
                    'mocked_cube.vtx[1]': [0.5, 0.5, 0.5],
                    'mocked_cube.vtx[2]': [-0.5, 1.5, 0.5],
                    'mocked_cube.vtx[3]': [0.5, 1.5, 0.5],
                    'mocked_cube.vtx[4]': [-0.5, 1.5, -0.5],
                    'mocked_cube.vtx[5]': [0.5, 1.5, -0.5],
                    'mocked_cube.vtx[6]': [-0.5, 0.5, -0.5],
                    'mocked_cube.vtx[7]': [0.5, 0.5, -0.5]}
        self.assertEqual(expected, result)

    def test_set_component_positions_from_dict_world_space(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')
        cmds.move(0, 1, 0, crv)

        component_dict = {'|mocked_curve.cv[0]': [0.0, 0.0, 2.0]}

        core_transform.set_component_positions_from_dict(component_pos_dict=component_dict, world_space=True)

        result = cmds.xform('|mocked_curve.cv[0]', worldSpace=True, query=True, translation=True)

        expected = [0.0, 0.0, 2.0]
        self.assertEqual(expected, result)

        component_dict = {'|mocked_curve.cv[0]': [0.0, 0.0, 3.0]}

        core_transform.set_component_positions_from_dict(component_pos_dict=component_dict, world_space=True)

        result = cmds.xform('|mocked_curve.cv[0]', worldSpace=True, query=True, translation=True)

        expected = [0.0, 0.0, 3.0]
        self.assertEqual(expected, result)

    def test_set_component_positions_from_dict_object_space(self):
        crv = cmds.curve(point=[[0.0, 0.0, 1.0], [0.0, 0.0, 0.667], [0.0, 0.0, 0.0],
                                                [0.0, 0.0, -1.0], [0.0, 0.0, -1.667], [0.0, 0.0, -2.0]],
                                         degree=3, name='mocked_curve')
        cmds.move(0, 1, 0, crv)

        component_dict = {'|mocked_curve.cv[0]': [0.0, 0.0, 2.0]}

        core_transform.set_component_positions_from_dict(component_pos_dict=component_dict,
                                                         world_space=False)  # False = Object Space

        result = cmds.xform('|mocked_curve.cv[0]', worldSpace=True, query=True, translation=True)

        expected = [0.0, 1.0, 2.0]
        self.assertEqual(expected, result)

        component_dict = {'|mocked_curve.cv[0]': [0.0, 0.0, 3.0]}

        core_transform.set_component_positions_from_dict(component_pos_dict=component_dict,
                                                         world_space=False)  # False = Object Space

        result = cmds.xform('|mocked_curve.cv[0]', worldSpace=True, query=True, translation=True)

        expected = [0.0, 1.0, 3.0]
        self.assertEqual(expected, result)

    def test_get_directional_position_object_does_not_exist(self):
        object_name = "non_existing_object"
        logging.disable(logging.WARNING)
        result = core_transform.get_directional_position(object_name=object_name)
        logging.disable(logging.NOTSET)
        expected = 0
        self.assertEqual(expected, result)

    def test_get_directional_position_invalid_axis(self):
        cube = maya_test_tools.create_poly_cube(name="cube_one")
        invalid_axis = "invalid_axis"
        logging.disable(logging.WARNING)
        result = core_transform.get_directional_position(object_name=cube, axis=invalid_axis)
        logging.disable(logging.NOTSET)
        expected = 0
        self.assertEqual(expected, result)

    def test_get_directional_position_negative(self):
        cube = maya_test_tools.create_poly_cube(name="cube_one")
        cmds.setAttr(f'{cube}.tx', -10)
        result = core_transform.get_directional_position(object_name=cube, axis="X", tolerance=0.001)
        expected = -1
        self.assertEqual(expected, result)

    def test_get_directional_position_positive(self):
        cube = maya_test_tools.create_poly_cube(name="cube_one")
        cmds.setAttr(f'{cube}.tx', 10)
        result = core_transform.get_directional_position(object_name=cube, axis="X", tolerance=0.001)
        expected = 1
        self.assertEqual(expected, result)

    def test_get_directional_position_center(self):
        cube = maya_test_tools.create_poly_cube(name="cube_one")
        result = core_transform.get_directional_position(object_name=cube, axis="X", tolerance=0.001)
        expected = 0
        self.assertEqual(expected, result)

    def test_get_directional_position_tolerance(self):
        cube_one = maya_test_tools.create_poly_cube(name="cube_one")
        cube_two = maya_test_tools.create_poly_cube(name="cube_two")
        cmds.setAttr(f'{cube_one}.tx', 0.05)
        result = core_transform.get_directional_position(object_name=cube_one, axis="X", tolerance=0.001)
        expected = 1
        self.assertEqual(expected, result)
        result = core_transform.get_directional_position(object_name=cube_one, axis="X", tolerance=0.1)
        expected = 0
        self.assertEqual(expected, result)
        result = core_transform.get_directional_position(object_name=cube_two, axis="X", tolerance=0.1)
        expected = 0
        self.assertEqual(expected, result)
        result = core_transform.get_directional_position(object_name=cube_two, axis="X", tolerance=0) # No Center
        expected = 1
        self.assertEqual(expected, result)
        result = core_transform.get_directional_position(object_name=cube_one, axis="X", tolerance=0) # No Center
        expected = 1
        self.assertEqual(expected, result)
        cmds.setAttr(f'{cube_one}.tx', -0.05)
        result = core_transform.get_directional_position(object_name=cube_one, axis="X", tolerance=0) # No Center
        expected = -1
        self.assertEqual(expected, result)
