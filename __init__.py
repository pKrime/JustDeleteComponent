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
import bmesh
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
        order = ['VERT', 'EDGE', 'FACE']
        mode = context.tool_settings.mesh_select_mode

        selected_verts = []
        selected_edges = []

        prefs = bpy.context.preferences.addons[__package__].preferences
        if prefs.multi_policy == 'FEV':
            order.reverse()
            indexed_modes = zip(range(len(order) - 1, -1, -1), order)

            if mode[2]:
                bm = bmesh.from_edit_mesh(context.object.data)
                vertices= [v for v in bm.verts]
                edges = [e for e in bm.edges]

                if not mode[0]:
                    selected_edges = [e.index for e in edges if e.select]

                if not selected_edges:
                    selected_verts = [v.index for v in vertices if v.select]
        else:
            indexed_modes = zip(range(len(order)), order)

        for i, sel_type in indexed_modes:
            if mode[i]:
                bpy.ops.mesh.delete(type=sel_type)

            for edge in selected_edges:
                bm.edges[edge].select = True
                selected_edges.clear()

        for vert in selected_verts:
            bm.verts[vert].select = True





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



