import os
import sys
import logging
import unittest

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
from gt.core import color as core_color
cmds = maya_test_tools.cmds


class TestColorCore(unittest.TestCase):
    def setUp(self):
        maya_test_tools.force_new_scene()

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

    def test_color_constants_rgb_class(self):
        attributes = vars(core_color.ColorConstants.RGB)
        keys = [attr for attr in attributes if not (attr.startswith('__') and attr.endswith('__'))]
        for clr_key in keys:
            color = getattr(core_color.ColorConstants.RGB, clr_key)
            if not color:
                raise Exception(f'Missing color: {clr_key}')
            if not isinstance(color, tuple):
                raise Exception(f'Incorrect color type. Expected tuple, but got: "{type(color)}".')
            if len(color) != 3:
                raise Exception(f'Incorrect color length. Expected 3, but got: "{str(len(color))}".')

    def test_color_constants_rig_proxy_class(self):
        attributes = vars(core_color.ColorConstants.RigProxy)
        keys = [attr for attr in attributes if not (attr.startswith('__') and attr.endswith('__'))]
        for clr_key in keys:
            color = getattr(core_color.ColorConstants.RigProxy, clr_key)
            if not color:
                raise Exception(f'Missing color: {clr_key}')
            if not isinstance(color, tuple):
                raise Exception(f'Incorrect color type. Expected tuple, but got: "{type(color)}".')
            if len(color) != 3:
                raise Exception(f'Incorrect color length. Expected 3, but got: "{str(len(color))}".')

    def test_color_constants_rig_control_class(self):
        attributes = vars(core_color.ColorConstants.RigControl)
        keys = [attr for attr in attributes if not (attr.startswith('__') and attr.endswith('__'))]
        for clr_key in keys:
            color = getattr(core_color.ColorConstants.RigControl, clr_key)
            if not color:
                raise Exception(f'Missing color: {clr_key}')
            if not isinstance(color, tuple):
                raise Exception(f'Incorrect color type. Expected tuple, but got: "{type(color)}".')
            if len(color) != 3:
                raise Exception(f'Incorrect color length. Expected 3, but got: "{str(len(color))}".')

    def test_color_constants_rig_joint_class(self):
        attributes = vars(core_color.ColorConstants.RigJoint)
        keys = [attr for attr in attributes if not (attr.startswith('__') and attr.endswith('__'))]
        for clr_key in keys:
            color = getattr(core_color.ColorConstants.RigJoint, clr_key)
            if not color:
                raise Exception(f'Missing color: {clr_key}')
            if not isinstance(color, tuple):
                raise Exception(f'Incorrect color type. Expected tuple, but got: "{type(color)}".')
            if len(color) != 3:
                raise Exception(f'Incorrect color length. Expected 3, but got: "{str(len(color))}".')

    def test_set_color_viewport(self):
        cube_one = maya_test_tools.create_poly_cube(name='test_cube_one')
        expected_color = (0, 0.5, 1)
        result = core_color.set_color_viewport(obj_list=cube_one, rgb_color=expected_color)
        expected_result = [cube_one]
        self.assertEqual(expected_result, result)
        set_color = cmds.getAttr(f'{cube_one}.overrideColorRGB')[0]
        self.assertEqual(expected_color, set_color)
        override_state = cmds.getAttr(f'{cube_one}.overrideEnabled')
        self.assertTrue(override_state, "Expected override to be enabled.")

    def test_set_color_viewport_list(self):
        cube_one = maya_test_tools.create_poly_cube(name='test_cube_one')
        cube_two = maya_test_tools.create_poly_cube(name='test_cube_two')
        expected_color = (0, 0.5, 1)
        result = core_color.set_color_viewport(obj_list=[cube_one, cube_two],
                                               rgb_color=expected_color)
        expected_result = [cube_one, cube_two]
        self.assertEqual(expected_result, result)
        for obj in [cube_one, cube_two]:
            set_color = cmds.getAttr(f'{obj}.overrideColorRGB')[0]
            self.assertEqual(expected_color, set_color)
            override_state = cmds.getAttr(f'{obj}.overrideEnabled')
            self.assertTrue(override_state, "Expected override to be enabled.")

    def test_set_color_outliner(self):
        cube_one = maya_test_tools.create_poly_cube(name='test_cube_one')
        expected_color = (0, 0.5, 1)
        result = core_color.set_color_outliner(obj_list=cube_one, rgb_color=expected_color)
        expected_result = [cube_one]
        self.assertEqual(expected_result, result)
        clr_r = cmds.getAttr(f'{cube_one}.outlinerColorR')
        clr_g = cmds.getAttr(f'{cube_one}.outlinerColorG')
        clr_b = cmds.getAttr(f'{cube_one}.outlinerColorB')
        self.assertEqual(expected_color, (clr_r, clr_g, clr_b))
        override_state = cmds.getAttr(f'{cube_one}.useOutlinerColor')
        self.assertTrue(override_state, "Expected override to be enabled.")

    def test_set_color_outliner_list(self):
        cube_one = maya_test_tools.create_poly_cube(name='test_cube_one')
        cube_two = maya_test_tools.create_poly_cube(name='test_cube_two')
        expected_color = (0, 0.5, 1)
        result = core_color.set_color_outliner(obj_list=[cube_one, cube_two],
                                               rgb_color=expected_color)
        expected_result = [cube_one, cube_two]
        self.assertEqual(expected_result, result)
        for obj in [cube_one, cube_two]:
            clr_r = cmds.getAttr(f'{obj}.outlinerColorR')
            clr_g = cmds.getAttr(f'{obj}.outlinerColorG')
            clr_b = cmds.getAttr(f'{obj}.outlinerColorB')
            self.assertEqual(expected_color, (clr_r, clr_g, clr_b))
            override_state = cmds.getAttr(f'{obj}.useOutlinerColor')
            self.assertTrue(override_state, "Expected override to be enabled.")

    def test_apply_gamma_correction_to_rgb(self):
        expected_color = (.2, .3, 1)
        result = core_color.apply_gamma_correction_to_rgb(rgb_color=expected_color)
        expected = (0.0289, 0.0707, 1.0)
        for index in range(0, 3):
            self.assertAlmostEqualSigFig(expected[index], result[index])

    def test_remove_gamma_correction_from_rgb(self):
        expected_color = (.2, .3, 1)
        result = core_color.remove_gamma_correction_from_rgb(rgb_color=expected_color)
        expected = (0.4811, 0.5785, 1.0)
        for index in range(0, 3):
            self.assertAlmostEqualSigFig(expected[index], result[index])

    def test_apply_remove_gamma_correction_from_rgb(self):
        expected_color = (.2, .3, 1)
        result = core_color.apply_gamma_correction_to_rgb(rgb_color=expected_color)
        result = core_color.remove_gamma_correction_from_rgb(rgb_color=result)
        expected = (.2, .3, 1)
        for index in range(0, 3):
            self.assertAlmostEqualSigFig(expected[index], result[index])

    def test_add_side_color_setup(self):
        test_obj = 'test_cube'
        maya_test_tools.create_poly_cube(name=test_obj)

        core_color.add_side_color_setup(obj=test_obj, color_attr_name="autoColor")

        expected_bool_attrs = ['autoColor']
        expected_double_attrs = ['colorDefault', 'colorRight', 'colorLeft']
        for attr in expected_bool_attrs + expected_double_attrs:
            self.assertTrue(cmds.objExists(f'{test_obj}.{attr}'),
                            f'Missing expected attribute: "{attr}".')

        expected = 'bool'
        for attr in expected_bool_attrs:
            attr_type = cmds.getAttr(f'{test_obj}.{attr}', type=True)
            self.assertEqual(expected, attr_type)
        expected = 'double3'
        for attr in expected_double_attrs:
            attr_type = cmds.getAttr(f'{test_obj}.{attr}', type=True)
            self.assertEqual(expected, attr_type)

        expected = True
        result = cmds.getAttr(f'{test_obj}.overrideEnabled')
        self.assertEqual(expected, result)
        expected = 1
        result = cmds.getAttr(f'{test_obj}.overrideRGBColors')
        self.assertEqual(expected, result)

    def test_get_directional_color_x_center(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')

        result = core_color.get_directional_color(object_name=cube, axis="X")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.CENTER
        self.assertEqual(expected, result)

    def test_get_directional_color_x_neg_left(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tx', -5)
        result = core_color.get_directional_color(object_name=cube, axis="X")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.RIGHT
        self.assertEqual(expected, result)

    def test_get_directional_color_x_pos_right(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tx', 5)
        result = core_color.get_directional_color(object_name=cube, axis="X")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.LEFT
        self.assertEqual(expected, result)

    def test_get_directional_color_y_center(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')

        result = core_color.get_directional_color(object_name=cube, axis="Y")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.CENTER
        self.assertEqual(expected, result)

    def test_get_directional_color_y_pos(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.ty', 5)
        result = core_color.get_directional_color(object_name=cube, axis="Y")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.LEFT
        self.assertEqual(expected, result)

    def test_get_directional_color_y_neg(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.ty', -5)
        result = core_color.get_directional_color(object_name=cube, axis="Y")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.RIGHT
        self.assertEqual(expected, result)

    def test_get_directional_color_z_center(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        result = core_color.get_directional_color(object_name=cube, axis="Z")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.CENTER
        self.assertEqual(expected, result)

    def test_get_directional_color_z_neg(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tz', -5)
        result = core_color.get_directional_color(object_name=cube, axis="Z")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.RIGHT
        self.assertEqual(expected, result)

    def test_get_directional_color_z_pos(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tz', 5)
        result = core_color.get_directional_color(object_name=cube, axis="Z")
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.LEFT
        self.assertEqual(expected, result)

    def test_get_directional_color_change(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        result = core_color.get_directional_color(object_name=cube, axis="Z",
                                                  negative_color=(1, 0, 0),
                                                  center_color=(0, 1, 0),
                                                  positive_color=(0, 0, 1))
        expected = (0, 1, 0)
        self.assertEqual(expected, result)

        cmds.setAttr(f'{cube}.tz', 5)
        result = core_color.get_directional_color(object_name=cube, axis="Z",
                                                  negative_color=(1, 0, 0),
                                                  center_color=(0, 1, 0),
                                                  positive_color=(0, 0, 1))
        expected = (0, 0, 1)
        self.assertEqual(expected, result)

        cmds.setAttr(f'{cube}.tz', -5)
        result = core_color.get_directional_color(object_name=cube, axis="Z",
                                                  negative_color=(1, 0, 0),
                                                  center_color=(0, 1, 0),
                                                  positive_color=(0, 0, 1))
        expected = (1, 0, 0)
        self.assertEqual(expected, result)

    def test_get_directional_color_tolerance(self):
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tx', 0.05)
        result = core_color.get_directional_color(object_name=cube, axis="X", tolerance=0.1)
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.CENTER
        self.assertEqual(expected, result)
        cube = maya_test_tools.create_poly_cube(name='test_cube')
        cmds.setAttr(f'{cube}.tx', 0.11)
        result = core_color.get_directional_color(object_name=cube, axis="X", tolerance=0.1)
        from gt.core.color import ColorConstants
        expected = ColorConstants.RigControl.LEFT
        self.assertEqual(expected, result)
