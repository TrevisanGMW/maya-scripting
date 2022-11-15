"""
 GT Blend Utilities
 github.com/TrevisanGMW/gt-tools - 2020-11-15

 0.0.1 to 0.0.2 - 2020-11-15
 Added "delete_blends_target"
 Added "delete_blends_targets"
 Added "delete_all_blend_targets"

 TODO:
    Add search/replace renamer
    Add error handling

"""
import maya.cmds as cmds
import logging

# Logging Setup
logging.basicConfig()
logger = logging.getLogger("gt_blend_utilities")
logger.setLevel(logging.INFO)

# Script Name
script_name = "GT - Blend Utilities"

# Version:
script_version = "0.0.2"


def delete_blends_targets(blend_node):
    """
    Delete all blend targets found in the provided blend shape node

    Args:
        blend_node (string) Name of the blend shape node
    """
    cmds.select(d=True)  # Deselect
    blendshape_names = cmds.listAttr(blend_node + '.w', m=True)
    for i in range(len(blendshape_names)):
        cmds.removeMultiInstance(blend_node + ".weight[" + str(i) + "]", b=True)
        cmds.removeMultiInstance(blend_node + ".inputTarget[0].inputTargetGroup[" + str(i) + "]", b=True)


def delete_all_blend_targets():
    """
    Delete all blend shape targets (not the nodes, only the targets)
    Dependencies:
        delete_blends_targets()
    """
    cmds.select(d=True)  # Deselect
    for blend_node in cmds.ls(typ="blendShape"):
        delete_blends_targets(blend_node)


def delete_blends_target(blend_node, target_name):
    """
    Deletes only the provided blend target
    Args:
        blend_node (string) Name of the blend shape node
        target_name (string) Name of the blend shape target to delete
    """
    cmds.select(d=True)  # Deselect
    blendshape_names = cmds.listAttr(blend_node + '.w', m=True)

    for i in range(len(blendshape_names)):
        if blendshape_names[i] == target_name:
            cmds.removeMultiInstance(blend_node + ".weight[" + str(i) + "]", b=True)
            cmds.removeMultiInstance(blend_node + ".inputTarget[0].inputTargetGroup[" + str(i) + "]", b=True)


def delete_blend_nodes(obj):
    """
    Deletes any blend shape nodes found under the history of the provided object

    Args:
        obj (String): name of the object. e.g. "pSphere1"
    """
    history = cmds.listHistory(obj)
    for node in history:
        if cmds.objectType(node) == "blendShape":
            cmds.delete(node)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    first_selection = cmds.ls(selection=True)[0]
    delete_blend_nodes(first_selection)
