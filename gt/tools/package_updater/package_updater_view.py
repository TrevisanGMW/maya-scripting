"""
Package Updater Window
"""

import gt.ui.resource_library as ui_res_lib
import gt.ui.qt_utils as ui_qt_utils
import gt.ui.qt_import as ui_qt


class PackageUpdaterView(metaclass=ui_qt_utils.MayaWindowMeta):
    def __init__(self, parent=None, controller=None, version=None):
        """
        Initialize the PackageUpdater.
        This window represents the main GUI window of the tool.

        Args:
            parent (str): Parent for this window
            controller (PackageUpdaterController): PackageUpdaterController, not to be used, here so it's not deleted
                                                   by the garbage collector.  Defaults to None.
            version (str, optional): If provided, it will be used to determine the window title. e.g. Title - (v1.2.3)
        """
        super().__init__(parent=parent)

        self.controller = controller  # Only here so it doesn't get deleted by the garbage collectors
        # Labels
        self.title_label = None
        self.status_label = None
        self.status_label = None
        self.web_response_label = None
        self.installed_version_label = None
        self.latest_release_label = None
        self.changelog_label = None
        # Content
        self.status_content = None
        self.web_response_content = None
        self.installed_version_content = None
        self.latest_release_content = None
        # Buttons
        self.update_btn = None
        self.refresh_btn = None
        self.auto_check_btn = None
        self.interval_btn = None
        # Misc
        self.changelog_box = None

        window_title = "Package Updater"
        if version:
            window_title += f" - (v{str(version)})"
        self.setWindowTitle(window_title)

        self.create_widgets()
        self.create_layout()

        self.setWindowFlags(
            self.windowFlags()
            | ui_qt.QtLib.WindowFlag.WindowMaximizeButtonHint
            | ui_qt.QtLib.WindowFlag.WindowMinimizeButtonHint
        )
        self.setWindowIcon(ui_qt.QtGui.QIcon(ui_res_lib.Icon.tool_package_updater))

        stylesheet = ui_res_lib.Stylesheet.scroll_bar_base
        stylesheet += ui_res_lib.Stylesheet.maya_dialog_base
        stylesheet += ui_res_lib.Stylesheet.list_widget_base
        self.setStyleSheet(stylesheet)
        self.update_btn.setStyleSheet(ui_res_lib.Stylesheet.btn_push_bright)
        ui_qt_utils.resize_to_screen(self, percentage=35, width_percentage=30)
        ui_qt_utils.center_window(self)
        # self.setWindowFlag(QtCore.Qt.Tool, True)  # Stay On Top Modality - Fixes Mac order issue

    def create_widgets(self):
        """Create the widgets for the window."""
        self.title_label = ui_qt.QtWidgets.QLabel("GT-Tools - Package Updater")
        self.title_label.setStyleSheet(
            "background-color: rgb(93, 93, 93); border: 0px solid rgb(93, 93, 93); \
                                        color: rgb(255, 255, 255); padding: 0px; margin-bottom: 15"
        )
        self.status_label = ui_qt.QtWidgets.QLabel("Status:")
        self.status_content = ui_qt.QtWidgets.QLabel("<status>")

        self.web_response_label = ui_qt.QtWidgets.QLabel("Web Response:")
        self.web_response_content = ui_qt.QtWidgets.QLabel("<web-response>")

        self.installed_version_label = ui_qt.QtWidgets.QLabel("Installed Version:")
        self.installed_version_content = ui_qt.QtWidgets.QLabel("<installed-version>")

        self.latest_release_label = ui_qt.QtWidgets.QLabel("Latest Release:")
        self.latest_release_content = ui_qt.QtWidgets.QLabel("<latest-version>")

        self.changelog_label = ui_qt.QtWidgets.QLabel("Latest Release Changelog:")
        self.changelog_label.setStyleSheet(
            f"font-weight: bold; font-size: 8; margin-top: 15; " f"color: {ui_res_lib.Color.RGB.gray_lighter};"
        )

        self.changelog_box = ui_qt.QtWidgets.QTextEdit()
        self.changelog_box.setFont(ui_qt_utils.load_custom_font(ui_res_lib.Font.roboto, point_size=9))
        self.changelog_box.setMinimumHeight(150)
        self.changelog_box.setReadOnly(True)

        # Set Alignment Center
        for label in [
            self.title_label,
            self.status_label,
            self.status_content,
            self.web_response_label,
            self.web_response_content,
            self.installed_version_label,
            self.installed_version_content,
            self.latest_release_label,
            self.latest_release_content,
            self.changelog_label,
        ]:
            label.setAlignment(ui_qt.QtLib.AlignmentFlag.AlignCenter)
            label.setFixedHeight(label.sizeHint().height() * 1.5)
            label.setFont(ui_qt_utils.get_font(ui_res_lib.Font.roboto))

        self.changelog_label.setFixedHeight(35)
        self.status_content.setFixedWidth(label.sizeHint().width())
        self.web_response_content.setFixedWidth(label.sizeHint().width())
        self.installed_version_content.setFixedWidth(label.sizeHint().width())
        self.latest_release_content.setFixedWidth(label.sizeHint().width())

        self.changelog_box.setSizePolicy(
            self.changelog_box.sizePolicy().Expanding, self.changelog_box.sizePolicy().Expanding
        )

        self.auto_check_btn = ui_qt.QtWidgets.QPushButton("Auto Check: Activated")
        self.auto_check_btn.setStyleSheet("padding: 10;")
        self.auto_check_btn.setToolTip("Change Check for Updates State (Activated/Deactivated)")
        self.interval_btn = ui_qt.QtWidgets.QPushButton("Interval: 15 Days")
        self.interval_btn.setStyleSheet("padding: 10;")
        self.interval_btn.setToolTip("Change Check for Updates Interval")
        self.refresh_btn = ui_qt.QtWidgets.QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("padding: 10; margin-bottom: 2;")
        self.refresh_btn.setToolTip("Check Github Again for New Updates")
        self.update_btn = ui_qt.QtWidgets.QPushButton("Update")
        self.update_btn.setToolTip("Download and Install Latest Update")
        self.update_btn.setEnabled(False)

    def create_layout(self):
        """Create the layout for the window."""
        top_layout = ui_qt.QtWidgets.QHBoxLayout()
        top_left_widget = ui_qt.QtWidgets.QVBoxLayout()
        top_right_widget = ui_qt.QtWidgets.QVBoxLayout()
        top_layout.addLayout(top_left_widget)
        top_layout.addLayout(top_right_widget)

        top_left_widget.addWidget(self.status_label)
        top_left_widget.addWidget(self.web_response_label)
        top_left_widget.addWidget(self.installed_version_label)
        top_left_widget.addWidget(self.latest_release_label)

        top_right_widget.addWidget(self.status_content)
        top_right_widget.addWidget(self.web_response_content)
        top_right_widget.addWidget(self.installed_version_content)
        top_right_widget.addWidget(self.latest_release_content)
        top_right_widget.setAlignment(ui_qt.QtLib.AlignmentFlag.AlignCenter)

        bottom_layout = ui_qt.QtWidgets.QVBoxLayout()
        bottom_layout.addWidget(self.changelog_label)
        bottom_layout.addWidget(self.changelog_box)

        settings_buttons_layout = ui_qt.QtWidgets.QHBoxLayout()
        settings_buttons_layout.addWidget(self.auto_check_btn)
        settings_buttons_layout.addWidget(self.interval_btn)
        settings_buttons_layout.setContentsMargins(0, 5, 0, 2)
        bottom_layout.addLayout(settings_buttons_layout)
        bottom_layout.addWidget(self.refresh_btn)
        bottom_layout.addWidget(self.update_btn)

        main_layout = ui_qt.QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Make Margins Uniform LTRB
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

    def change_update_button_state(self, state):
        """
        Change the state of the "Update" button
        Args:
            state (bool): New state of the button: Disable/Enable the button True = Active, False = Inactive.
        """
        if isinstance(state, bool):
            self.update_btn.setEnabled(state)

    def change_interval_button_state(self, state):
        """
        Change the state of the "Interval: <Number> days" button
        Args:
            state (bool): New state of the button: Disable/Enable the button True = Active, False = Inactive.
        """
        if isinstance(state, bool):
            self.interval_btn.setEnabled(state)

    def clear_changelog_box(self):
        """Removes all text from the changelog box"""
        self.changelog_box.clear()

    def add_text_to_changelog(self, text, text_color_hex=None):
        """
        Add text to the changelog_box with optional color selection.

        Args:
            text (str): The text to be added to the changelog_box.
            text_color_hex (str, optional): The color of the text in HEX format (e.g., '#FF0000'). Defaults to None.
        """
        cursor = self.changelog_box.textCursor()
        if text_color_hex:
            formatted_text = f'<span style="white-space: pre-line"><font color="{text_color_hex}">{text}</font></span>'
        else:
            formatted_text = text

        cursor.movePosition(ui_qt.QtLib.TextCursor.End)
        cursor.insertHtml(formatted_text)
        cursor.insertText("\n")  # Add a new line

        self.changelog_box.setTextCursor(cursor)
        # Move to the top
        cursor = ui_qt.QtGui.QTextCursor(self.changelog_box.document())
        cursor.movePosition(ui_qt.QtLib.TextCursor.Start)
        self.changelog_box.setTextCursor(cursor)

    @staticmethod
    def update_label(label_obj, text, text_color_hex=None, bg_color_hex=None):
        """
        Update the status content and its background color.
        This method updates the content and background color of a QLabel used
        to display status information.

        Args:
            label_obj (QLabel): QLabel object to update
            text (str): The new text to be displayed.
            text_color_hex (str, optional): A hexadecimal color code for the text color. Default is None
            bg_color_hex (str, optional): A hexadecimal color code for the background color. Default is None

        Example:
            To update the status label with "OK" status and green background color:
            self.update_status("New Update Available!", "#00FF00")
        """
        label_obj.setText(text)
        stylesheet = ""
        if text_color_hex:
            stylesheet += f"color: {text_color_hex};"
        if bg_color_hex:
            stylesheet += f"background-color: {bg_color_hex};"
        if stylesheet:
            label_obj.setStyleSheet(stylesheet)

    def update_status(self, status, text_color_hex=None, bg_color_hex=None):
        """
        Updates the status content:
        Args:
            status (str): The new text to be displayed as status.
            text_color_hex (str, optional): A hexadecimal color code for the text color. Default is None
            bg_color_hex (str, optional): A hexadecimal color code for the background color. Default is None
        """
        self.update_label(self.status_content, status, text_color_hex=text_color_hex, bg_color_hex=bg_color_hex)

    def update_web_response(self, response, text_color_hex=None, bg_color_hex=None):
        """
        Updates the status content:
        Args:
            response (str): The new text to be displayed as web-response.
            text_color_hex (str, optional): A hexadecimal color code for the text color. Default is None
            bg_color_hex (str, optional): A hexadecimal color code for the background color. Default is None
        """
        self.update_label(self.web_response_content, response, text_color_hex=text_color_hex, bg_color_hex=bg_color_hex)

    def update_installed_version(self, version, text_color_hex=None, bg_color_hex=None):
        """
        Updates the status content:
        Args:
            version (str): The new text to be displayed as the installed version.
            text_color_hex (str, optional): A hexadecimal color code for the text color. Default is None
            bg_color_hex (str, optional): A hexadecimal color code for the background color. Default is None
        """
        self.update_label(
            self.installed_version_content, version, text_color_hex=text_color_hex, bg_color_hex=bg_color_hex
        )

    def update_latest_release(self, version, text_color_hex=None, bg_color_hex=None):
        """
        Updates the status content:
        Args:
            version (str): The new text to be displayed as the installed version.
            text_color_hex (str, optional): A hexadecimal color code for the text color. Default is None
            bg_color_hex (str, optional): A hexadecimal color code for the background color. Default is None
        """
        self.update_label(
            self.latest_release_content, version, text_color_hex=text_color_hex, bg_color_hex=bg_color_hex
        )

    def update_auto_check_status_btn(self, is_active):
        """
        Updates the status content:
        Args:
            is_active (bool): New status. True is activated, false is deactivated
        """
        title = "Auto Check: "
        if is_active:
            self.auto_check_btn.setText(f"{title}Activated")
        else:
            self.auto_check_btn.setText(f"{title}Deactivated")

    def update_interval_button(self, time_period):
        """
        Updates the status content:
        Args:
            time_period (str): Number of days to update the interval button with.
        """
        if time_period:
            self.interval_btn.setText(f"Interval: {str(time_period)}")

    def close_window(self):
        """Closes this window"""
        self.close()


if __name__ == "__main__":
    with ui_qt_utils.QtApplicationContext():
        window = PackageUpdaterView(version="1.2.3")  # View
        window.change_update_button_state(state=False)
        window.add_text_to_changelog("hello hello helo hello")
        window.add_text_to_changelog("hello hello helo hello", text_color_hex="#0000FF")
        window.update_status("New Update Available!", text_color_hex="black", bg_color_hex="#FF7F7F")
        window.update_web_response("OK")
        window.update_installed_version("v1.2.3")
        window.update_latest_release("v4.5.6")
        window.update_auto_check_status_btn(False)
        window.update_interval_button(5)
        window.change_interval_button_state(False)
        window.show()
