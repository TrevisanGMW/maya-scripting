import json
import os
import sys
import logging
import unittest
from unittest.mock import patch, MagicMock

# Logging Setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Import Tested Utility and Maya Test Tools
test_utils_dir = os.path.dirname(__file__)
tests_dir = os.path.dirname(test_utils_dir)
package_root_dir = os.path.dirname(tests_dir)
for to_append in [package_root_dir, tests_dir]:
    if to_append not in sys.path:
        sys.path.append(to_append)
from tests import maya_test_tools
from gt.utils import data_utils


class TestDataUtils(unittest.TestCase):
    def setUp(self):
        self.mocked_str = "mocked_data"
        self.mocked_dict = {"mocked_key_a": "mocked_value_a",
                            "mocked_key_b": "mocked_value_b"}
        self.temp_dir = maya_test_tools.generate_test_temp_dir()
        self.file_path = os.path.join(self.temp_dir, "test_file.txt")

    def tearDown(self):
        maya_test_tools.delete_test_temp_dir()

    def assert_file_content_equal(self, file_path, expected_content):
        """
        Asserts that the content of a file at the specified file path is equal to the expected content.

        Parameters:
            file_path (str): The path to the file whose content needs to be checked.
            expected_content (str): The expected content that the file should contain.

        Raises:
            AssertionError: If the content of the file does not match the expected content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            self.assertEqual(content, expected_content)

    def assert_json_file_content_equal(self, file_path, expected_content):
        """
        Asserts that the content of a JSON file at the specified file path is equal to the expected content.

        Parameters:
            file_path (str): The path to the JSON file whose content needs to be checked.
            expected_content (dict or list): The expected JSON content that the file should contain.
                                            It can be either a dictionary or a list.

        Raises:
            AssertionError: If the content of the JSON file does not match the expected content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                json_content = json.load(file)
            except json.JSONDecodeError:
                raise AssertionError(f"Invalid JSON file: {file_path}")
        self.assertEqual(json_content, expected_content)

    def test_write_data_return(self):
        data = self.mocked_str
        returned_path = data_utils.write_data(self.file_path, data)
        expected = self.file_path
        self.assertEqual(expected, returned_path)

    def test_write_data_missing_file(self):
        data = self.mocked_str
        logging.disable(logging.WARNING)
        returned_path = data_utils.write_data("mocked_non_existing_path/mocked_file.txt", data)
        logging.disable(logging.NOTSET)
        expected = None
        self.assertEqual(expected, returned_path)

    def test_write_data_content(self):
        data = self.mocked_str
        returned_path = data_utils.write_data(self.file_path, data)
        self.assert_file_content_equal(file_path=returned_path, expected_content=data)

    def test_read_data_content(self):
        data = self.mocked_str
        with open(self.file_path, "w", encoding="utf-8") as data_file:
            data_file.write(data)  # Write Data to Temp File
        result = data_utils.read_data(self.file_path)  # Read Data from Temp File
        self.assertEqual(data, result)

    def test_read_data_content_missing_file(self):
        logging.disable(logging.WARNING)
        result = data_utils.read_data("mocked_non_existing_path/mocked_file.txt")
        logging.disable(logging.NOTSET)
        expected = None
        self.assertEqual(expected, result)

    def test_write_json_return(self):
        data = self.mocked_dict
        returned_path = data_utils.write_json(self.file_path, data)
        expected = self.file_path
        self.assertEqual(expected, returned_path)

    def test_write_json_missing_file(self):
        data = self.mocked_dict
        logging.disable(logging.WARNING)
        returned_path = data_utils.write_json("mocked_non_existing_path/mocked_file.txt", data)
        logging.disable(logging.NOTSET)
        expected = None
        self.assertEqual(expected, returned_path)

    def test_write_json_content(self):
        data = self.mocked_dict
        returned_path = data_utils.write_json(self.file_path, data)
        self.assert_json_file_content_equal(file_path=returned_path, expected_content=data)

    def test_read_json_content(self):
        data = self.mocked_dict
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json_file.write(json_data)  # Write JSON Data to Temp File
        result = data_utils.read_json_dict(self.file_path)  # Read JSON Data from Temp File
        self.assertEqual(data, result)

    def test_read_json_content_missing_file(self):
        logging.disable(logging.WARNING)
        result = data_utils.read_json_dict("mocked_non_existing_path/mocked_file.txt")
        logging.disable(logging.NOTSET)
        expected = {}
        self.assertEqual(expected, result)
