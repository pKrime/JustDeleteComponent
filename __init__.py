# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Just Delete Component",
    "author": "Paolo Acampora",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Mesh > Just Delete",
    "description": "Delete components according to current selection mode",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}


import bpy
from . import preferences

from . import __refresh__
__refresh__.reload_modules()


class MESH_OT_just_delete_component(bpy.types.Operator):
    """Delete component according to selection"""
    bl_idname = "mesh.just_delete"
    bl_label = "Just Delete"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(cls, context):
        ob = context.object
        
        if not ob:
            return False

        return ob.type == 'MESH' and ob.mode == 'EDIT'

    def execute(self, context):
        mode = context.tool_settings.mesh_select_mode

        # TODO revert if prefs "ALL"
        if mode[2]:
            bpy.ops.mesh.delete(type='FACE')
        if mode[1]:
            bpy.ops.mesh.delete(type='EDGE')
        if mode[0]:
            bpy.ops.mesh.delete(type='VERT')

        return {'FINISHED'}


def add_delete_to_menu(self, context):
    self.layout.operator(
        MESH_OT_just_delete_component.bl_idname,
        text="Just Delete")


def register():
    preferences.register_classes()
    bpy.utils.register_class(MESH_OT_just_delete_component)
    bpy.types.VIEW3D_MT_edit_mesh.append(add_delete_to_menu)

    preferences.register_shortcut(MESH_OT_just_delete_component.bl_idname)



def unregister():
    
    preferences.unregister_classes()

    bpy.utils.unregister_class(MESH_OT_just_delete_component)
    bpy.types.VIEW3D_MT_edit_mesh.remove(add_delete_to_menu)


if __name__ == "__main__":
    register()



