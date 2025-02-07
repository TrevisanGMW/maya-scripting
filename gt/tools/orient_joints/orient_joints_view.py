"""
Orient Joints View/Window
"""

import gt.ui.resource_library as ui_res_lib
import gt.ui.qt_utils as ui_qt_utils
import gt.ui.qt_import as ui_qt


class OrientJointsView(metaclass=ui_qt_utils.MayaWindowMeta):
    def __init__(self, parent=None, controller=None, version=None):
        """
        Initialize the OrientJointsView.
        This window represents the main GUI window of the tool.

        Args:
            parent (str): Parent for this window
            controller (OrientJointsViewController): OrientJointsViewController, not to be used, here so
                                                          it's not deleted by the garbage collector.  Defaults to None.
            version (str, optional): If provided, it will be used to determine the window title. e.g. Title - (v1.2.3)
        """
        super().__init__(parent=parent)

        self.controller = controller  # Only here so it doesn't get deleted by the garbage collectors

        # Window Title
        self.window_title = "Orient Joints"
        _window_title = self.window_title
        if version:
            _window_title += f" - (v{str(version)})"
        self.setWindowTitle(_window_title)

        self.utilities_label = None
        self.settings_label = None
        self.target_label = None
        self.aim_axis_label = None
        self.up_axis_label = None
        self.up_dir_label = None

        # Buttons
        self.show_axis_btn = None
        self.hide_axis_btn = None
        self.copy_parent_btn = None
        self.copy_world_btn = None
        self.orient_joints_btn = None

        # Radial Btn Groups
        self.target_grp = None
        self.target_selected = None
        self.target_hierarchy = None

        self.aim_axis_grp = None
        self.aim_axis_x = None
        self.aim_axis_y = None
        self.aim_axis_z = None

        self.up_axis_grp = None
        self.up_axis_x = None
        self.up_axis_y = None
        self.up_axis_z = None

        self.up_dir_grp = None
        self.up_dir_x = None
        self.up_dir_y = None
        self.up_dir_z = None

        # Combo Boxes
        self.aim_axis_mod = None
        self.up_axis_mod = None
        self.up_dir_mod = None

        self.create_widgets()
        self.create_layout()

        self.setWindowFlags(
            self.windowFlags()
            | ui_qt.QtLib.WindowFlag.WindowMaximizeButtonHint
            | ui_qt.QtLib.WindowFlag.WindowMinimizeButtonHint
        )
        self.setWindowIcon(ui_qt.QtGui.QIcon(ui_res_lib.Icon.tool_orient_joints))

        stylesheet = ui_res_lib.Stylesheet.scroll_bar_base
        stylesheet += ui_res_lib.Stylesheet.maya_dialog_base
        stylesheet += ui_res_lib.Stylesheet.list_widget_base
        stylesheet += ui_res_lib.Stylesheet.btn_radio_base
        stylesheet += ui_res_lib.Stylesheet.combobox_base
        self.setStyleSheet(stylesheet)

        self.show_axis_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_base)
        self.hide_axis_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_base)
        self.orient_joints_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_bright)
        self.hide_axis_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_base)
        self.copy_parent_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_base)
        self.copy_world_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_base)

        # Initial Selection (Default)
        self.target_selected.setChecked(True)
        self.aim_axis_x.setChecked(True)
        self.up_axis_y.setChecked(True)
        self.up_dir_y.setChecked(True)

        ui_qt_utils.resize_to_screen(self, percentage=20, width_percentage=30)
        ui_qt_utils.center_window(self)

    def create_widgets(self):
        """Create the widgets for the window."""
        self.utilities_label = ui_qt.QtWidgets.QLabel("Utilities:")
        self.utilities_label.setStyleSheet(
            f"font-weight: bold; font-size: 8; margin-top: 0; " f"color: {ui_res_lib.Color.RGB.gray_lighter};"
        )

        self.utilities_label.setAlignment(ui_qt.QtLib.AlignmentFlag.AlignCenter)
        self.utilities_label.setFont(ui_qt_utils.get_font(ui_res_lib.Font.roboto))
        self.utilities_label.setFixedHeight(self.utilities_label.sizeHint().height())

        self.settings_label = ui_qt.QtWidgets.QLabel("Orientation Settings:")
        self.settings_label.setStyleSheet(
            f"font-weight: bold; font-size: 8; margin-top: 0; " f"color: {ui_res_lib.Color.RGB.gray_lighter};"
        )
        self.settings_label.setAlignment(ui_qt.QtLib.AlignmentFlag.AlignCenter)
        self.settings_label.setFont(ui_qt_utils.get_font(ui_res_lib.Font.roboto))
        self.settings_label.setFixedHeight(self.settings_label.sizeHint().height())

        self.show_axis_btn = ui_qt.QtWidgets.QPushButton("Show Axis")
        self.show_axis_btn.setToolTip("Set the visibility of the local rotation axis to on (active)")
        self.show_axis_btn.setStyleSheet("padding: 10;")

        self.hide_axis_btn = ui_qt.QtWidgets.QPushButton("Hide Axis")
        self.hide_axis_btn.setToolTip("Set the visibility of the local rotation axis to off (inactive)")
        self.hide_axis_btn.setStyleSheet("padding: 10;")

        self.copy_parent_btn = ui_qt.QtWidgets.QPushButton("Copy Parent")
        self.copy_parent_btn.setToolTip("Match orientation of the parent")
        self.copy_parent_btn.setStyleSheet("padding: 10;")

        self.copy_world_btn = ui_qt.QtWidgets.QPushButton("Reset to World")
        self.copy_world_btn.setToolTip("Match orientation of the world (origin)")
        self.copy_world_btn.setStyleSheet("padding: 10;")

        self.target_grp = ui_qt.QtWidgets.QButtonGroup()
        self.target_label = ui_qt.QtWidgets.QLabel("Target:")
        self.target_selected = ui_qt.QtWidgets.QRadioButton("Selected")
        self.target_hierarchy = ui_qt.QtWidgets.QRadioButton("Hierarchy")
        self.target_grp.addButton(self.target_selected)
        self.target_grp.addButton(self.target_hierarchy)
        self.aim_axis_label = ui_qt.QtWidgets.QLabel("Aim Axis:")
        self.aim_axis_grp = ui_qt.QtWidgets.QButtonGroup()
        self.aim_axis_x = ui_qt.QtWidgets.QRadioButton("X")
        self.aim_axis_y = ui_qt.QtWidgets.QRadioButton("Y")
        self.aim_axis_z = ui_qt.QtWidgets.QRadioButton("Z")
        self.aim_axis_grp.addButton(self.aim_axis_x)
        self.aim_axis_grp.addButton(self.aim_axis_y)
        self.aim_axis_grp.addButton(self.aim_axis_z)
        self.up_axis_label = ui_qt.QtWidgets.QLabel("Up Axis:")
        self.up_axis_grp = ui_qt.QtWidgets.QButtonGroup()
        self.up_axis_x = ui_qt.QtWidgets.QRadioButton("X")
        self.up_axis_y = ui_qt.QtWidgets.QRadioButton("Y")
        self.up_axis_z = ui_qt.QtWidgets.QRadioButton("Z")
        self.up_axis_grp.addButton(self.up_axis_x)
        self.up_axis_grp.addButton(self.up_axis_y)
        self.up_axis_grp.addButton(self.up_axis_z)
        self.up_dir_label = ui_qt.QtWidgets.QLabel("Up Dir:")
        self.up_dir_grp = ui_qt.QtWidgets.QButtonGroup()
        self.up_dir_x = ui_qt.QtWidgets.QRadioButton("X")
        self.up_dir_y = ui_qt.QtWidgets.QRadioButton("Y")
        self.up_dir_z = ui_qt.QtWidgets.QRadioButton("Z")
        self.up_dir_grp.addButton(self.up_dir_x)
        self.up_dir_grp.addButton(self.up_dir_y)
        self.up_dir_grp.addButton(self.up_dir_z)

        self.aim_axis_mod = ui_qt.QtWidgets.QComboBox()
        self.up_axis_mod = ui_qt.QtWidgets.QComboBox()
        self.up_dir_mod = ui_qt.QtWidgets.QComboBox()
        for combobox in [self.aim_axis_mod, self.up_axis_mod, self.up_dir_mod]:
            combobox.addItem("+")
            combobox.addItem("-")
            combobox.setMaximumWidth(50)
            combobox.setMinimumWidth(50)

        self.orient_joints_btn = ui_qt.QtWidgets.QPushButton("Orient Joints")
        self.orient_joints_btn.setStyleSheet("padding: 10;")

    def create_layout(self):
        """Create the layout for the window."""
        utility_layout = ui_qt.QtWidgets.QVBoxLayout()
        utility_layout.addWidget(self.utilities_label)
        axis_layout = ui_qt.QtWidgets.QHBoxLayout()
        axis_layout.addWidget(self.show_axis_btn)
        axis_layout.addWidget(self.hide_axis_btn)
        copy_layout = ui_qt.QtWidgets.QHBoxLayout()
        copy_layout.addWidget(self.copy_parent_btn)
        copy_layout.addWidget(self.copy_world_btn)
        utility_layout.addLayout(axis_layout)
        utility_layout.addLayout(copy_layout)

        self.show_axis_btn.setSizePolicy(ui_qt.QtLib.SizePolicy.Expanding, ui_qt.QtLib.SizePolicy.Expanding)
        self.hide_axis_btn.setSizePolicy(ui_qt.QtLib.SizePolicy.Expanding, ui_qt.QtLib.SizePolicy.Expanding)
        self.copy_parent_btn.setSizePolicy(ui_qt.QtLib.SizePolicy.Expanding, ui_qt.QtLib.SizePolicy.Expanding)
        self.copy_world_btn.setSizePolicy(ui_qt.QtLib.SizePolicy.Expanding, ui_qt.QtLib.SizePolicy.Expanding)

        separator = ui_qt.QtWidgets.QFrame()
        separator.setFrameShape(ui_qt.QtLib.FrameStyle.HLine)
        separator.setFrameShadow(ui_qt.QtLib.FrameStyle.Sunken)

        body_layout = ui_qt.QtWidgets.QVBoxLayout()
        body_layout.addWidget(self.settings_label)

        target_layout = ui_qt.QtWidgets.QGridLayout()
        target_layout.addWidget(self.target_label, 0, 0)
        target_layout.addWidget(self.target_selected, 0, 1)
        target_layout.addWidget(self.target_hierarchy, 0, 2)
        body_layout.addLayout(target_layout)

        aim_axis_layout = ui_qt.QtWidgets.QGridLayout()
        aim_axis_layout.addWidget(self.aim_axis_label, 0, 0)
        aim_axis_layout.addWidget(self.aim_axis_x, 0, 1)
        aim_axis_layout.addWidget(self.aim_axis_y, 0, 2)
        aim_axis_layout.addWidget(self.aim_axis_z, 0, 3)
        aim_axis_layout.addWidget(self.aim_axis_mod, 0, 4)
        body_layout.addLayout(aim_axis_layout)

        up_axis_layout = ui_qt.QtWidgets.QGridLayout()
        up_axis_layout.addWidget(self.up_axis_label, 0, 0)
        up_axis_layout.addWidget(self.up_axis_x, 0, 1)
        up_axis_layout.addWidget(self.up_axis_y, 0, 2)
        up_axis_layout.addWidget(self.up_axis_z, 0, 3)
        up_axis_layout.addWidget(self.up_axis_mod, 0, 4)
        body_layout.addLayout(up_axis_layout)

        up_dir_layout = ui_qt.QtWidgets.QGridLayout()
        up_dir_layout.addWidget(self.up_dir_label, 0, 0)
        up_dir_layout.addWidget(self.up_dir_x, 0, 1)
        up_dir_layout.addWidget(self.up_dir_y, 0, 2)
        up_dir_layout.addWidget(self.up_dir_z, 0, 3)
        up_dir_layout.addWidget(self.up_dir_mod, 0, 4)
        body_layout.addLayout(up_dir_layout)
        body_layout.setContentsMargins(20, 5, 20, 5)  # L-T-R-B

        action_layout = ui_qt.QtWidgets.QVBoxLayout()
        action_layout.addWidget(self.orient_joints_btn)

        main_layout = ui_qt.QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        top_layout = ui_qt.QtWidgets.QVBoxLayout()
        mid_layout = ui_qt.QtWidgets.QVBoxLayout()
        bottom_layout = ui_qt.QtWidgets.QVBoxLayout()
        top_layout.setContentsMargins(15, 15, 15, 15)  # L-T-R-B
        mid_layout.setContentsMargins(15, 0, 15, 15)  # L-T-R-B
        bottom_layout.setContentsMargins(15, 0, 15, 15)  # L-T-R-B
        top_layout.addLayout(utility_layout)
        mid_layout.addLayout(body_layout)
        bottom_layout.addLayout(action_layout)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(mid_layout)
        main_layout.addLayout(bottom_layout)

    @staticmethod
    def _get_mod_value_as_int(combobox):
        """
        Converts the modifier combobox value into an integer
        Returns:
            int: An integer representing the value to be used in the vector.
                 If "+" = 1, if "-" = -1
        """
        combobox_text = combobox.currentText()
        _value = 1
        if combobox_text == "-":
            _value = -1
        return _value

    def get_aim_axis_tuple(self):
        """
        Gets a tuple with the aim axis data. e.g. (1, 0, 0) = X+
        Returns:
            tuple: A tuple describing the aim axis data
        """
        aim_axis_buttons = self.aim_axis_grp.buttons()
        _mod_value = self._get_mod_value_as_int(self.aim_axis_mod)
        _aim_list = []
        for btn in aim_axis_buttons:
            if btn.isChecked():
                _aim_list.append(_mod_value)
            else:
                _aim_list.append(0)
        return tuple(_aim_list)

    def get_up_axis_tuple(self):
        """
        Gets a tuple with the up axis data. e.g. (1, 0, 0) = X+
        Returns:
            tuple: A tuple describing the up axis data
        """
        up_axis_buttons = self.up_axis_grp.buttons()
        _mod_value = self._get_mod_value_as_int(self.up_axis_mod)
        _up_list = []
        for btn in up_axis_buttons:
            if btn.isChecked():
                _up_list.append(_mod_value)
            else:
                _up_list.append(0)
        return tuple(_up_list)

    def get_up_dir_tuple(self):
        """
        Gets a tuple with the up dir data. e.g. (1, 0, 0) = X+
        Returns:
            tuple: A tuple describing the up dir data
        """
        up_dir_buttons = self.up_dir_grp.buttons()
        _mod_value = self._get_mod_value_as_int(self.up_dir_mod)
        _up_dir_list = []
        for btn in up_dir_buttons:
            if btn.isChecked():
                _up_dir_list.append(_mod_value)
            else:
                _up_dir_list.append(0)
        return tuple(_up_dir_list)

    def is_selecting_hierarchy(self):
        """
        Determines if the user is using hierarchy as selection.
        Returns:
            bool: True if the selection target is "hierarchy"
        """
        return self.target_hierarchy.isChecked()


if __name__ == "__main__":
    with ui_qt_utils.QtApplicationContext():
        window = OrientJointsView(version="1.2.3")  # View
        window.show()
        window.orient_joints_btn.clicked.connect(window.is_selecting_hierarchy)
