"""
Alembic Module

Code Namespace:
    core_alembic  # import gt.core.alembic as core_alembic
"""

from gt.core.transform import Transform, Vector3
from math import degrees
import maya.cmds as cmds
import logging

# Logging Setup
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_alembic_plugin(include_alembic_bullet=False):
    """
    Attempt to load alembic plugins (required for export/import operations)
    Args:
        include_alembic_bullet (optional, bool): If active, the plugin "AbcBullet" is included in the loading operation
    Returns:
        True if all alembic plugins were successfully loaded, False if something is missing
    """
    plugins_to_load = ["AbcExport", "AbcImport"]
    if include_alembic_bullet:
        plugins_to_load.append("AbcBullet")
    plugins_loaded = []

    # Load Plug-in
    for plugin in plugins_to_load:
        if not cmds.pluginInfo(plugin, q=True, loaded=True):
            try:
                cmds.loadPlugin(plugin)
                if cmds.pluginInfo(plugin, q=True, loaded=True):
                    plugins_loaded.append(plugin)
            except Exception as e:
                logger.debug(f'Unable to load plugin "{plugin}". Plugin is likely not installed. Issue: {e}')
        else:
            plugins_loaded.append(plugin)

    if len(plugins_loaded) == len(plugins_to_load):
        return True
    else:
        return False


def get_alembic_nodes():
    """
    Get a list of alembic nodes in the scene
    Returns:
        List of alembic nodes in the scene. Empty list if nothing was found.
    """
    return cmds.ls(typ="AlembicNode", long=True) or []


def get_alembic_cycle_as_string(alembic_node):
    """
    Returns alembic cycle as a string (instead of number)
    Args:
        alembic_node (str): Name of the alembic alembic_node (must be an alembic alembic_node)
    Returns:
        str: String describing cycle type. None if failed to retrieve
    """
    cycle_string = ["Hold", "Loop", "Reverse", "Bounce"]
    if not cmds.objExists(f"{alembic_node}.cycleType"):
        logger.debug(
            f"Unable to get cycle as string. Missing alembic alembic_node attribute: " f'"{alembic_node}.cycle_type".'
        )
        return
    alembic_cycle = cmds.getAttr(f"{alembic_node}.cycleType")
    if alembic_cycle is not None and alembic_cycle <= len(cycle_string):
        return cycle_string[alembic_cycle]
    else:
        logger.debug(f'Unable to get cycle as string. "cmds.getAttr" returned: {alembic_cycle}')
        return


class AlembicNode:
    name: str
    time: int
    offset: int
    start_time: int
    end_time: int
    cycle_type: str
    transform: Transform
    mesh_cache: str
    # keyframes: Keyframes

    def __init__(self, alembic_node):
        self.name = alembic_node
        self.time = cmds.getAttr(f"{alembic_node}.time")
        self.offset = cmds.getAttr(f"{alembic_node}.offset")
        self.start_time = cmds.getAttr(f"{alembic_node}.startFrame")
        self.end_time = cmds.getAttr(f"{alembic_node}.endFrame")
        self.cycle_type = get_alembic_cycle_as_string(alembic_node)
        self.transform = self.get_root_transform(alembic_node)
        self.mesh_cache = cmds.getAttr(f"{alembic_node}.abc_File")
        # self.keyframes = get_keyframes()

    @staticmethod
    def get_root_node(alembic_node):
        """
        List transform nodes found under the future history of the alembic node then returns the last
        node of the type "transform". If no transforms are found, the alembic node is returned instead.
        Args:
            alembic_node (str): Name of the alembic node (must exist)
        Returns:
            str: Last transform node found in the future history of the alembic node.
                 If nothing is found, the alembic node is returned instead.
        """
        root_node = alembic_node
        for history in cmds.listHistory(alembic_node, future=True):
            if cmds.objectType(history) == "transform":
                root_node = history
        return root_node

    def get_root_transform(self, alembic_node):
        root = self.get_root_node(alembic_node)
        try:
            translation = cmds.xform(root, q=True, ws=True, translation=True)
            rotation = cmds.xform(root, q=True, ws=True, rotation=True)
            scale = cmds.xform(root, q=True, ws=True, scale=True)
        except Exception as e:
            logger.debug(f"Unable to retrieve root transforms. Origin returned instead. Issue: {e}")
            return Transform()
        trans = Transform()
        trans.set_position(xyz=translation)
        rot = Vector3(x=degrees(rotation[0]), y=degrees(rotation[1]), z=degrees(rotation[2]))
        trans.set_rotation(xyz=rot)
        trans.set_scale(xyz=scale)
        return trans


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    from pprint import pprint

    # import maya.standalone
    # maya.standalone.initialize()
    node = get_alembic_nodes()[0]
    alembic = AlembicNode(node)
    out = None
    out = alembic.transform
    pprint(out)
