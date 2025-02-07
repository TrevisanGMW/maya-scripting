"""
Curve To Python Controller
"""
from gt.core.curve import get_python_shape_code, get_python_curve_code
from gt.utils.system import execute_python_code
from gt.core.misc import create_shelf_button
from gt.core.feedback import FeedbackMessage
import logging

# Logging Setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CurveToPythonController:
    def __init__(self, view, model=None):
        """
        Initialize the CurveToPythonController object.

        Args:
            view: The view object to interact with the user interface.
            model: The CurveToPythonModel object used for data manipulation.
        """
        self.model = model
        self.view = view
        self.view.controller = self

        # # Connections
        self.view.help_btn.clicked.connect(self.open_help)
        self.view.extract_crv_python_btn.clicked.connect(self.extract_crv_python)
        self.view.extract_shape_state_btn.clicked.connect(self.extract_crv_state)
        self.view.run_code_btn.clicked.connect(self.run_python_code)
        self.view.save_to_shelf_btn.clicked.connect(self.save_python_to_shelf)
        self.view.show()

    @staticmethod
    def open_help():
        """ Opens package docs """
        from gt.utils.request import open_package_docs_url_in_browser
        open_package_docs_url_in_browser()

    @staticmethod
    def __get_selection():
        """
        Gets selection while warning the user in case nothing is elected
        Returns:
         list: Selection or empty list when nothing is selected.
        """
        import maya.cmds as cmds
        selection = cmds.ls(selection=True) or []
        if len(selection) == 0:
            cmds.warning(f'Please select at least one curve and try again.')
            return []
        return selection

    def extract_crv_python(self):
        """
        Extracts the TRS channels as setAttr commands and populates the python output box with the extracted content.
        """
        selection = self.__get_selection()
        if not selection:
            return
        _code = "import maya.cmds as cmds\n\n"
        _code += get_python_curve_code(crv_list=selection)
        self.view.clear_python_output()
        self.view.set_python_output_text(text=_code)

    def extract_crv_state(self):
        """
        Extracts the TRS channels as lists and populates the python output box with the extracted content.
        """
        selection = self.__get_selection()
        if not selection:
            return
        _code = "import maya.cmds as cmds\n\n"
        _code += get_python_shape_code(crv_list=selection)
        self.view.clear_python_output()
        self.view.set_python_output_text(text=_code)

    def run_python_code(self):
        """
        Attempts to run the code found in the "Python Output" box.
        """
        _code = self.view.get_python_output_text()
        execute_python_code(code=_code, use_maya_warning=True, import_cmds=True)

    def save_python_to_shelf(self):
        """
        Saves the content of the python output box to a shelf button.
        """
        import maya.cmds as cmds
        _code = self.view.get_python_output_text()
        if _code:
            create_shelf_button(_code,
                                label='setAttr',
                                tooltip='Extracted Attributes',
                                image="editRenderPass.png",
                                label_color=(0, .84, .81))

            highlight_style = "color:#FF0000;text-decoration:underline;"
            feedback = FeedbackMessage(prefix='Python code',
                                       style_prefix=highlight_style,
                                       conclusion='was added as a button to your current shelf.')
            feedback.print_inview_message()
        else:
            cmds.warning('Unable to save to shelf. "Output Python Code" is empty.')


if __name__ == "__main__":
    print('Run it from "__init__.py".')
