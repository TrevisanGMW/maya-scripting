import shutil

try:
    import maya.cmds as cmds
    import maya.OpenMaya as OpenMaya
    import maya.api.OpenMaya as om
    import maya.mel as mel
except ModuleNotFoundError:
    from gt.tests.maya_test_tools.maya_spoof import MayaCmdsSpoof as cmds
    from gt.tests.maya_test_tools.maya_spoof import OpenMayaSpoof as OpenMaya
    from gt.tests.maya_test_tools.maya_spoof import OpenMayaApiSpoof as om
    from gt.tests.maya_test_tools.maya_spoof import MayaMelSpoof as mel

import logging
import inspect
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def force_new_scene():
    """
    Force open new empty scene
    """
    cmds.file(new=True, force=True)


def create_poly_cube(*args, **kwargs):
    """
    Creates poly cube
    "polyCube" relevant parameters:
        name (str): Name of the poly cube
    Returns:
        str or None: First item in the output list of the "cmds.polyCube" command. None if the output was empty.
    """
    cube = cmds.polyCube(*args, **kwargs) or []
    if cube and len(cube) >= 1:
        return cube[0]
    return None


def create_poly_sphere(*args, **kwargs):
    """
    Creates poly sphere
    "polySphere" relevant parameters:
        name (str): Name of the poly sphere
    Returns:
        str or None: First item in the output list of the "cmds.polySphere" command. None if the output was empty.
    """
    sphere = cmds.polySphere(*args, **kwargs) or []
    if sphere and len(sphere) >= 1:
        return sphere[0]
    return None


def create_poly_cylinder(*args, **kwargs):
    """
    Creates poly cylinder
    "polyCylinder" relevant parameters:
        name (str): Name of the poly cylinder
    Returns:
        str or None: First item in the output list of the "cmds.polyCylinder" command. None if the output was empty.
    """
    cylinder = cmds.polyCylinder(*args, **kwargs) or []
    if cylinder and len(cylinder) >= 1:
        return cylinder[0]
    return None


def create_group(name="group", *args, **kwargs):
    """
    Creates an empty group parented to the world with an optional predetermined name.
    "polyCylinder" relevant parameters:
        name (str): Name of the group
    Returns:
        str: Name of the created group
    """
    group = cmds.group(*args, **kwargs, name=name, empty=True, world=True)
    return group


def list_obj_types(obj_list):
    """
    Returns a dictionary with the object types
    Args:
        obj_list (list): List of objects. e.g. ["pCube1", "pCube2"]
    Returns:
        dict: A dictionary with object name as key and object type as value.
    """
    obj_types = {}
    for obj in obj_list:
        if obj and cmds.objExists(obj):
            obj_types[obj] = cmds.objectType(obj)
    return obj_types


def get_data_dir_path(module=None):
    """
    Get a path to the data folder using the path from where this script was called.
    NOTE: It does NOT return the expected path when called from inside a function in this same module.
    Args:
        module (module, optional): Module object used to define source path. If not provided caller is used.
    Returns:
        Path to the data folder of the caller script.
        pattern:  ".../<caller-script-dir>/data"
        e.g. If the function was called from a script inside "test_core"
             then the output would be ".../test_core/data"
             ("..." being the variable portion of the directory path)
    """
    if not module:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
    script_path = os.path.abspath(module.__file__)
    return os.path.join(os.path.dirname(script_path), "data")


def generate_test_temp_dir(folder_name="test_temp_dir"):
    """
    Creates a temporary directory used for testing. If already existing, it will only return the path to it.
    Args:
        folder_name (str, optional): Name of the folder to create. Default: "test_temp_dir"
    Returns:
        str: Path ".../test_core/data/test_temp_dir"
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    data_folder = get_data_dir_path(module=module)
    test_temp_dir = os.path.join(data_folder, folder_name)  # e.g. ".../data/test_temp_dir"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    if not os.path.exists(test_temp_dir):
        os.mkdir(test_temp_dir)
    return test_temp_dir


def delete_test_temp_dir(folder_name="test_temp_dir", auto_delete_empty_data_dir=True):
    """
    Deletes the temporary directory used for testing. (Only if existing)
    Args:
        folder_name (str, optional): Name of the folder to delete. Default: "test_temp_dir"
        auto_delete_empty_data_dir (bool, optional): If active, it will delete the data when it's empty.
    Returns:
        bool: True if it was deleted, False in case it was not found.
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    data_folder = get_data_dir_path(module=module)
    test_temp_dir = os.path.join(data_folder, folder_name)  # e.g. ".../data/test_temp_dir"
    if os.path.exists(test_temp_dir):
        shutil.rmtree(test_temp_dir)
        if auto_delete_empty_data_dir:
            data_content = os.listdir(data_folder)
            if len(data_content) == 0:
                shutil.rmtree(data_folder)
        return True
    return False


def unlock_file_permissions(file_path):
    """
    Unlocks write permissions for all users on the specified file.

    Args:
        file_path (str): The path to the file whose permissions need to be unlocked.

    Raises:
        OSError: If there was an issue accessing or modifying the file's permissions.

    Note:
        This function uses the `os` and `stat` modules to manipulate file permissions.
        The function will attempt to unlock write permissions for the owner, group, and
        other users of the specified file.

    Example:
        unlock_file_permissions('/path/to/file.txt')
        # If successful, the write permissions for all users on 'file.txt' are unlocked.
    """
    try:
        os.chmod(file_path, 0o700)
    except Exception as e:
        logger.debug(f"Unable to unlock file permissions. Issue: {e}")


def is_plugin_loaded(plugin):
    """
    Load provided plug-ins.

    Args:
        plugin (str): Name of the plugin to check
    Returns:
        bool: True if the plug is active, false if it's inactive.
    """
    return cmds.pluginInfo(plugin, q=True, loaded=True)


def load_plugins(plugin_list):
    """
    Load provided plug-ins.

    Args:
        plugin_list (list): A list of strings containing the name of the plugins that should be loaded.
                            If a string is provided, it will be automatically converted to a list
    Returns:
        list: A list of plugins that were loaded. (Plugins that were already loaded are not included in the list)
    """
    if isinstance(plugin_list, str):
        plugin_list = [plugin_list]

    now_loaded = []

    # Load Plug-in
    for plugin in plugin_list:
        if not is_plugin_loaded(plugin):
            try:
                cmds.loadPlugin(plugin)
                if is_plugin_loaded(plugin):
                    now_loaded.append(plugin)
            except Exception as e:
                logger.debug(e)
    return now_loaded


def unload_plugins(plugin_list):
    """
    Load provided plug-ins.

    Args:
        plugin_list (list): A list of strings containing the name of the plugins to  unloaded.
                            If a string is provided, it will be automatically converted to a list
    Returns:
        list: A list of plugins that were loaded. (Plugins that were already loaded are not included in the list)
    """
    if isinstance(plugin_list, str):
        plugin_list = [plugin_list]

    now_unloaded = []

    # Load Plug-in
    for plugin in plugin_list:
        if is_plugin_loaded(plugin):
            try:
                cmds.unloadPlugin(plugin)
                if not is_plugin_loaded(plugin):
                    now_unloaded.append(plugin)
            except Exception as e:
                logger.debug(e)
    return now_unloaded


def import_file(file_path):
    """
    Opens file_path in Maya using "cmds.file_path()"
    Args:
        file_path (str): Path to the file_path to open

    Returns:
        list: Imported objects. (result of the "cmds.file(returnNewNodes=True)" function)
    """
    if file_path.split(".")[-1] == "fbx":  # Make sure "fbxmaya" is available
        load_plugins(["fbxmaya"])
    elif file_path.split(".")[-1] == "abc":  # Make sure alembic is available
        load_plugins(["AbcExport", "AbcImport", "AbcBullet"])
    files = cmds.file(file_path, i=True, returnNewNodes=True, force=True)
    return files


def open_file(file_path):
    """
    Opens file in Maya using "cmds.file()"
    Args:
        file_path (str): Path to the file to open

    Returns:
        str: Opened file. (result of the "cmds.file()" function)

    """
    return cmds.file(file_path, open=True, force=True)


def get_data_file_path(file_name):
    """
    Gets the path to the data file from inside the test_*/data folder.
    It automatically determines the position of the data folder using the location where this function was called from.
    Args:
        file_name: Name of the file_path (must exist)
    Returns:
        str: Path to test data file.
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    script_path = get_data_dir_path(module=module)
    file_to_import = os.path.join(script_path, file_name)
    return file_to_import


def import_data_file(file_name):
    """
    Open files from inside the test_*/data folder.
    It automatically determines the position of the data folder using the location where this function was called from.
    Args:
        file_name: Name of the file_path (must exist)
    Returns:
        list: Imported objects. (result of the "cmds.file(returnNewNodes=True)" function)
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    script_path = get_data_dir_path(module=module)
    file_to_import = os.path.join(script_path, file_name)
    return import_file(file_to_import)  # Do not use "get_data_file_path",  it uses the function to retrieve path


def open_data_file(file_name):
    """
    Open files from inside the test_*/data folder.
    It automatically determines the position of the data folder using "get_data_dir_path()"
    Args:
        file_name: Name of the file (must exist)
    """
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    script_path = get_data_dir_path(module=module)
    file_to_import = os.path.join(script_path, file_name)
    return open_file(file_to_import)


def import_maya_standalone(initialize=True):
    """
    Imports Maya Standalone
    Args:
        initialize (bool, optional) If true, it will also attempt to initialize "maya.standalone" using "initialize()"
    """
    try:
        import maya.standalone as maya_standalone
    except ModuleNotFoundError:
        from gt.tests.maya_test_tools.maya_spoof import MayaStandaloneSpoof as maya_standalone
    if initialize:
        maya_standalone.initialize()


def set_scene_framerate(time):
    """
    Args:
    time (str): Sets the current scene frame rate
                    game: 15 fps
                    film: 24 fps
                    pal: 25 fps
                    ntsc: 30 fps
                    show: 48 fps
                    palf: 50 fps
                    ntscf: 60 fps
    Return:
        str: Result from the "cmds.currentUnit" operation (same as query)
    """
    return cmds.currentUnit(time=time)


def set_current_time(frame):
    """
    Set scene current time
    Args:
        frame (int): Frame where
    Returns:
        int: current time (frame) - Result of the "cmds.currentUnit" operation.
    """
    return cmds.currentTime(frame)


def eval_mel_code(mel_code_string):
    """
    Evaluates the given MEL (Maya Embedded Language) code string and returns the result.

    Args:
        mel_code_string (str): The MEL code string to be evaluated.

    Returns:
        Any: The result of evaluating the MEL code.

    Example:
        mel_code_string = "polyCube()"
        eval_mel_code(mel_code_string)
        Result: "pCube1"
    """
    return mel.eval(mel_code_string)


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    import maya.standalone

    maya.standalone.initialize()
    from pprint import pprint

    out = None
    # out = set_frame_rate("game")
    out = import_data_file("curves_nurbs_bezier.ma")
    pprint(out)
    pprint(cmds.ls())
