import gt.core.session as core_session
import gt.ui.qt_import as ui_qt


def file_dialog(
    caption="Open File",
    parent=None,
    write_mode=False,
    starting_directory=None,
    file_filter="All Files (*);;",
    dir_only=False,
    ok_caption="Open",
    cancel_caption="Cancel",
):
    """
    Shows a file dialog to open/select or write a file or directory.
    Args:
        ok_caption (str): Caption for the OK button.  (Only when in Maya)
        cancel_caption (str): Caption for the Cancel button.  (Only when in Maya)
        caption (str): Caption for the file dialog window. (Title of the window)
        write_mode (bool): If True, the dialog allows selecting or writing a file;
                           If False, it allows only selecting/opening.
        starting_directory (str, optional): The initial directory when the file dialog opens.
                                            (Also the pre-populated string for when in Maya)
        file_filter (str): Filter for file types to be displayed in the dialog.
                           Separate multiple filters use ";;" e.g. "All Files (*);;JSON Files (*.json)"
        dir_only (bool, optional): If True, the dialog allows selecting directories only;
                                   If False, it allows selecting files.
        parent: Parent widget. If not provided, it's automatically retrieved from the context.
    Returns:
        str: Path to the selected file/directory or empty string if cancelled.
    """
    if core_session.is_script_in_interactive_maya():  # Within Maya ----------------------------------
        import maya.cmds as cmds

        params = {
            "fileFilter": file_filter,
            "dialogStyle": 2,  # Use a custom file, which is consistent across platforms.,
            "fileMode": 1,  # Open File
            "okCaption": ok_caption,
            "cancelCaption": cancel_caption,
            "caption": caption,
        }
        # Determine File Mode
        if write_mode:
            params["fileMode"] = 0  # Write File
        if dir_only:
            params["fileMode"] = 2  # Directories Only
        if starting_directory and isinstance(starting_directory, str):
            params["startingDirectory"] = starting_directory

        file_name = cmds.fileDialog2(**params) or []
        if len(file_name) > 0:
            return file_name[0]
        return ""

    else:  # Outside Maya ----------------------------------------------------------------
        print("got here")
        options = ui_qt.QtWidgets.QFileDialog.Options()

        params = {
            "filter": file_filter,
            "caption": caption,
        }

        if starting_directory and isinstance(starting_directory, str):
            params["startingDirectory"] = starting_directory
        _file_dialog = ui_qt.QtWidgets.QFileDialog(parent=parent)
        if write_mode and not dir_only:  # Write File
            file_path, _ = _file_dialog.getSaveFileName(options=options, **params)
        elif dir_only:  # Dir Only
            file_path, _ = _file_dialog.getExistingDirectory(options=options, **params)
        else:
            file_path, _ = _file_dialog.getOpenFileName(options=options, **params)
        if file_path:
            return file_path
        else:
            return ""


if __name__ == "__main__":
    selected_file = file_dialog(file_filter="All Files (*);;JSON Files (*.json)")
    print(selected_file)
