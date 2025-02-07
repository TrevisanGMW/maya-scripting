from unittest.mock import patch
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
from tests import maya_test_tools
import gt.core.setup as core_setup


class TestSetupCore(unittest.TestCase):
    def setUp(self):
        maya_test_tools.force_new_scene()

    @classmethod
    def setUpClass(cls):
        maya_test_tools.import_maya_standalone(initialize=True)  # Start Maya Headless (mayapy.exe)

    def tearDown(self):
        maya_test_tools.delete_test_temp_dir()

    def test_get_maya_settings_dir_exists(self):
        settings_dir = core_setup.get_maya_preferences_dir()
        result = os.path.exists(settings_dir)
        expected = True
        self.assertEqual(expected, result)

    def test_get_maya_settings_dir_is_folder(self):
        settings_dir = core_setup.get_maya_preferences_dir()
        result = os.path.isdir(settings_dir)
        expected = True
        self.assertEqual(expected, result)

    @patch("maya.cmds.about")
    def test_get_maya_settings_dir_about_key(self, mock_about):
        mock_about.return_value = "mocked_path"
        core_setup.get_maya_preferences_dir()
        result = str(mock_about.call_args)
        expected = "call(preferences=True)"
        self.assertEqual(expected, result)

    def test_get_package_requirements_keys(self):
        result = core_setup.get_package_requirements()
        expected_items = ["gt"]
        for item in expected_items:
            self.assertIn(item, result)

    def test_get_package_requirements_path_exists(self):
        result_dict = core_setup.get_package_requirements()
        self.assertIsInstance(result_dict, dict)
        for value in result_dict.values():
            exists = os.path.exists(str(value))
            self.assertEqual(True, exists)

    def test_copy_package_requirements(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()  # Create test elements
        source_dir = os.path.join(test_temp_dir, "source_dir")
        target_dir = os.path.join(test_temp_dir, "target_dir")
        requirement_dir_one = os.path.join(source_dir, "dir_one")
        requirement_dir_two = os.path.join(source_dir, "dir_two")
        requirement_py = os.path.join(source_dir, "empty.py")
        undesired_pyc = os.path.join(source_dir, "empty.pyc")
        undesired_dir_one = os.path.join(requirement_dir_one, "__pycache__")
        undesired_dir_two = os.path.join(source_dir, "__pycache__")
        for path in [
            source_dir,
            target_dir,
            requirement_dir_one,
            requirement_dir_two,
            undesired_dir_one,
            undesired_dir_two,
        ]:
            if not os.path.exists(path):
                os.mkdir(path)
        for file in [requirement_py, undesired_pyc]:
            with open(file, "w"):
                pass  # Create empty file
        mocked_package_requirements = {
            "dir_one": str(requirement_dir_one),
            "dir_two": str(requirement_dir_two),
            "empty.py": str(requirement_py),
        }
        core_setup.copy_package_requirements(target_folder=target_dir, package_requirements=mocked_package_requirements)
        source_result = sorted(os.listdir(source_dir))
        source_expected = sorted(["dir_one", "dir_two", "empty.py", "empty.pyc", "__pycache__"])
        self.assertEqual(source_expected, source_result)
        target_result = sorted(os.listdir(target_dir))
        target_expected = sorted(["dir_one", "dir_two", "empty.py"])
        self.assertEqual(target_expected, target_result)

    def test_remove_previous_install(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()  # Create test elements
        mocked_install_dir = os.path.join(test_temp_dir, core_setup.PACKAGE_NAME)
        mocked_install_main_module = os.path.join(mocked_install_dir, core_setup.PACKAGE_MAIN_MODULE)
        from gt.core.prefs import PACKAGE_PREFS_DIR

        mocked_install_prefs = os.path.join(mocked_install_dir, PACKAGE_PREFS_DIR)
        mocked_pyc = os.path.join(mocked_install_dir, "empty.pyc")
        mocked_py = os.path.join(mocked_install_dir, "empty.py")
        for path in [mocked_install_dir, mocked_install_main_module, mocked_install_prefs]:
            if not os.path.exists(path):
                os.mkdir(path)
        for file in [mocked_pyc, mocked_py]:
            with open(file, "w"):
                pass  # Create empty file
        expected = True
        result = os.path.exists(mocked_install_main_module)
        self.assertEqual(expected, result)
        core_setup.remove_previous_install(target_path=mocked_install_dir)
        expected = False
        result = os.path.exists(mocked_install_main_module)
        self.assertEqual(expected, result)
        expected = True
        result = os.path.exists(mocked_install_dir)
        self.assertEqual(expected, result)

    def test_remove_previous_install_clear_prefs(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()  # Create test elements
        mocked_install_dir = os.path.join(test_temp_dir, core_setup.PACKAGE_NAME)
        mocked_install_main_module = os.path.join(mocked_install_dir, core_setup.PACKAGE_MAIN_MODULE)
        from gt.core.prefs import PACKAGE_PREFS_DIR

        mocked_install_prefs = os.path.join(mocked_install_dir, PACKAGE_PREFS_DIR)
        for path in [mocked_install_dir, mocked_install_main_module, mocked_install_prefs]:
            if not os.path.exists(path):
                os.mkdir(path)
        core_setup.remove_previous_install(target_path=mocked_install_dir, clear_prefs=True)
        expected = False
        result = os.path.exists(mocked_install_dir)
        self.assertEqual(expected, result)

    def test_check_installation_integrity(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()  # Create test elements
        for requirement in core_setup.PACKAGE_REQUIREMENTS:
            if "." in requirement:  # Assuming files have an extension
                with open(os.path.join(test_temp_dir, requirement), "w"):
                    pass
            else:
                dir_path = os.path.join(test_temp_dir, requirement)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
        for requirement in core_setup.PACKAGE_DIRS:
            if "." in requirement:  # Assuming files have an extension
                with open(os.path.join(test_temp_dir, core_setup.PACKAGE_MAIN_MODULE, requirement), "w"):
                    pass
            else:
                dir_path = os.path.join(test_temp_dir, core_setup.PACKAGE_MAIN_MODULE, requirement)
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
        result = core_setup.check_installation_integrity(package_target_folder=test_temp_dir)
        expected = True
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_invalid_preferences(self, mock_get_preferences):
        mock_get_preferences.return_value = {"1234": "invalid_path"}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=False)
        expected = []
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_not_existing(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=False)
        expected = [os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)]
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_existing_false(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=True)
        expected = []
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_existing_true(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w"):
            pass  # Create empty file
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=True)
        expected = [os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)]
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_add_entry_line_existing_default(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w"):
            pass  # Create empty file
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        core_setup.add_entry_line(file_path=mocked_file_name, create_missing_file=False)
        expected = [core_setup.PACKAGE_ENTRY_LINE + "\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_add_entry_line_not_existing(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        core_setup.add_entry_line(file_path=mocked_file_name, create_missing_file=True)
        expected = [core_setup.PACKAGE_ENTRY_LINE + "\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_add_entry_line_with_content(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write("# Mocked content")
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        core_setup.add_entry_line(file_path=mocked_file_name, create_missing_file=True)
        expected = ["# Mocked content\n", f"{core_setup.PACKAGE_ENTRY_LINE}\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_add_entry_line_missing(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        logging.disable(logging.WARNING)
        core_setup.add_entry_line(file_path=mocked_file_name, create_missing_file=False)
        logging.disable(logging.NOTSET)
        expected = False
        result = os.path.exists(mocked_file_name)
        self.assertEqual(expected, result)

    def test_remove_entry_line_basic(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"{core_setup.PACKAGE_ENTRY_LINE}\n")
        expected = [f"{core_setup.PACKAGE_ENTRY_LINE}\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)
        core_setup.remove_entry_line(
            file_path=mocked_file_name, line_to_remove=core_setup.PACKAGE_ENTRY_LINE, delete_empty_file=False
        )
        expected = []
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    def test_remove_entry_line_times_removed(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"{core_setup.PACKAGE_ENTRY_LINE}\n" * 5)
        result = core_setup.remove_entry_line(
            file_path=mocked_file_name, line_to_remove=core_setup.PACKAGE_ENTRY_LINE, delete_empty_file=False
        )
        expected = 5
        self.assertEqual(expected, result)

    def test_remove_entry_line_times_removed_zero(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w"):
            pass
        result = core_setup.remove_entry_line(
            file_path=mocked_file_name, line_to_remove=core_setup.PACKAGE_ENTRY_LINE, delete_empty_file=False
        )
        expected = 0
        self.assertEqual(expected, result)

    def test_remove_entry_line_delete_empty(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(core_setup.PACKAGE_ENTRY_LINE + "\n")
        expected = [core_setup.PACKAGE_ENTRY_LINE + "\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)
        core_setup.remove_entry_line(
            file_path=mocked_file_name, line_to_remove=core_setup.PACKAGE_ENTRY_LINE, delete_empty_file=True
        )
        expected = False
        result = os.path.exists(mocked_file_name)
        self.assertEqual(expected, result)

    def test_remove_entry_line_delete_non_empty(self):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_ENTRY_LINE}\n")
        result = core_setup.remove_entry_line(
            file_path=mocked_file_name, line_to_remove=core_setup.PACKAGE_ENTRY_LINE, delete_empty_file=True
        )
        expected = 1
        self.assertEqual(expected, result)
        expected = True
        result = os.path.exists(mocked_file_name)
        self.assertEqual(expected, result)

    @patch("gt.core.setup.generate_user_setup_list")
    def test_add_entry_point_to_maya_installs(self, mock_user_setup_list):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        mock_user_setup_list.return_value = [mocked_file_name]
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write("# Mocked content\n")
        core_setup.add_entry_point_to_maya_installs()
        expected = ["# Mocked content\n", f"{core_setup.PACKAGE_ENTRY_LINE}\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.generate_user_setup_list")
    def test_remove_entry_point_from_maya_installs(self, mock_user_setup_list):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        mock_user_setup_list.return_value = [mocked_file_name]
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_ENTRY_LINE}\n")
        core_setup.remove_entry_point_from_maya_installs()
        expected = ["# Mocked content\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.generate_user_setup_list")
    def test_remove_legacy_entry_point_from_maya_installs(self, mock_user_setup_list):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        mock_user_setup_list.return_value = [mocked_file_name]
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_LEGACY_LINE}\n")
        core_setup.remove_legacy_entry_point_from_maya_installs(verbose=False)
        expected = ["# Mocked content\n"]
        with open(mocked_file_name) as file:
            result = file.readlines()
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_return(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_LEGACY_LINE}\n")
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=True)
        expected = [mocked_file_name]
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_exists(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_LEGACY_LINE}\n")
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=True)
        expected = True
        if result:
            result = os.path.exists(result[0])
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_scripts_dir_list_non_existing(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_scripts_dir_list(file_name=core_setup.PACKAGE_USER_SETUP, only_existing=True)
        expected = []
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_generate_user_setup_list_return(self, mock_get_preferences):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, core_setup.PACKAGE_USER_SETUP)
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content\n{core_setup.PACKAGE_LEGACY_LINE}\n")
        mock_get_preferences.return_value = {"2020": test_temp_dir}
        result = core_setup.generate_user_setup_list(only_existing=True)
        expected = [mocked_file_name]
        self.assertEqual(expected, result)

    @patch("gt.core.setup.generate_scripts_dir_list")
    def test_copy_package_loader_to_maya_installs(self, mock_scripts_dir_list):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, "package_loader.py")
        mock_scripts_dir_list.return_value = [mocked_file_name]
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        core_setup.copy_package_loader_to_maya_installs()
        expected = True
        result = os.path.exists(mocked_file_name)
        self.assertEqual(expected, result)

    @patch("gt.core.setup.generate_scripts_dir_list")
    def test_remove_package_loader_from_maya_installs(self, mock_scripts_dir_list):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_scripts_dir = os.path.join(test_temp_dir, "scripts")
        mocked_file_name = os.path.join(mocked_scripts_dir, "package_loader.py")
        mock_scripts_dir_list.return_value = [mocked_file_name]
        if not os.path.exists(mocked_scripts_dir):
            os.mkdir(mocked_scripts_dir)
        with open(mocked_file_name, "w") as file:
            file.write(f"# Mocked content")
        core_setup.remove_package_loader_from_maya_installs()
        expected = False
        result = os.path.exists(mocked_file_name)
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_available_maya_preferences_dirs")
    def test_is_legacy_version_install_present(self, mocked_maya_preferences_dirs):
        mocked_maya_preferences_dirs.return_value = {}
        result = core_setup.is_legacy_version_install_present()
        expected = False
        self.assertEqual(expected, result)

    @patch("gt.core.setup.check_installation_integrity")
    @patch("gt.core.setup.remove_legacy_entry_point_from_maya_installs")
    @patch("gt.core.setup.copy_package_loader_to_maya_installs")
    @patch("gt.core.setup.add_entry_point_to_maya_installs")
    @patch("gt.core.setup.remove_previous_install")
    @patch("gt.core.setup.get_package_requirements")
    @patch("gt.core.setup.get_maya_preferences_dir")
    @patch("gt.core.setup.is_script_in_py_maya")
    def test_install_package_basic_calls(
        self,
        mock_is_script_in_py,
        mock_preferences_dir,
        mock_get_package_requirements,
        mock_remove_previous_install,
        mock_add_entry_point,
        mock_copy_package_loader,
        mock_remove_legacy_entry_point,
        mock_installation_integrity,
    ):
        maya_test_tools.mel.eval('$gMainWindow = "";')  # To avoid unnecessary UI error
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_target_dir = os.path.join(test_temp_dir, core_setup.PACKAGE_NAME)
        mocked_requirement_dir = os.path.join(test_temp_dir, "tools")
        if not os.path.exists(mocked_requirement_dir):
            os.mkdir(mocked_requirement_dir)
        mock_is_script_in_py.return_value = False  # Maya Standalone already initialized (True initializes it)
        mock_preferences_dir.return_value = test_temp_dir
        mock_get_package_requirements.return_value = {"tools": mocked_requirement_dir}
        result = core_setup.install_package(clean_install=True, verbose=False)
        mock_is_script_in_py.assert_called()
        mock_preferences_dir.assert_called()
        mock_get_package_requirements.assert_called_once()
        mock_remove_previous_install.assert_called_once()
        mock_add_entry_point.assert_called_once()
        mock_copy_package_loader.assert_called_once()
        mock_remove_legacy_entry_point.assert_called_once()
        mock_installation_integrity.assert_called_once()
        expected = True  # Ended with return True - Reached integrity check
        self.assertEqual(expected, result)
        expected = "tools"
        result = os.listdir(mocked_target_dir)
        self.assertIn(expected, result)

    @patch("gt.core.setup.remove_package_loader_from_maya_installs")
    @patch("gt.core.setup.remove_entry_point_from_maya_installs")
    @patch("gt.core.setup.get_maya_preferences_dir")
    @patch("gt.core.setup.is_script_in_py_maya")
    def test_uninstall_package_basic_calls(
        self, mock_is_script_in_py, mock_preferences_dir, mock_remove_entry_point, mock_remove_package_loader
    ):
        test_temp_dir = maya_test_tools.generate_test_temp_dir()
        mocked_target_dir = os.path.join(test_temp_dir, core_setup.PACKAGE_NAME)
        mocked_requirement_dir = os.path.join(test_temp_dir, "tools")
        if not os.path.exists(mocked_requirement_dir):
            os.mkdir(mocked_requirement_dir)
        if not os.path.exists(mocked_target_dir):
            os.mkdir(mocked_target_dir)
        mock_is_script_in_py.return_value = False  # Maya Standalone already initialized (True initializes it)
        mock_preferences_dir.return_value = test_temp_dir
        result = core_setup.uninstall_package(verbose=False)
        mock_is_script_in_py.assert_called()
        mock_preferences_dir.assert_called()
        mock_remove_entry_point.assert_called_once()
        mock_remove_package_loader.assert_called_once()
        expected = True  # Ended with return True reached end of function
        self.assertEqual(expected, result)
        expected = False
        result = os.path.exists(mocked_target_dir)
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_maya_preferences_dir")
    def test_get_installed_module_path(self, mocked_get_prefs):
        mocked_get_prefs.return_value = "mocked_path"
        result = core_setup.get_installed_core_module_path()
        expected = os.path.join("mocked_path", "gt-tools", "gt")
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_maya_preferences_dir")
    def test_get_installed_module_path_only_existing(self, mocked_get_prefs):
        mocked_get_prefs.return_value = "mocked_path"
        result = core_setup.get_installed_core_module_path(only_existing=True)
        expected = None
        self.assertEqual(expected, result)

    @patch("gt.core.setup.get_installed_core_module_path")
    def test_successful_prepend(self, mock_get_installed_core_module_path):
        mock_get_installed_core_module_path.return_value = "/path/to/installed/core/module"
        remove_paths = ["/some/old/path"]

        initial_sys_path = sys.path.copy()
        sys.path.insert(0, remove_paths[0])
        result = core_setup.prepend_sys_path_with_default_install_location(remove_paths)

        self.assertTrue(result)
        self.assertIn("/path/to/installed/core/module", sys.path)
        self.assertNotIn("/some/old/path", sys.path)

        # Clean up sys.path modifications
        sys.path = initial_sys_path
