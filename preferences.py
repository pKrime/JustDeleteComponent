import os

import bpy


def get_key_types():
    param = bpy.types.KeyMapItems.bl_rna.functions['new'].parameters['type']
    key_types = param.enum_items_static.keys()

    for i, k in enumerate(reversed(key_types)):
        if k.startswith('F') and k[-1].isdigit():
            continue
        if 'MOUSE' in k:
            continue
        if 'BUTTON' in k:
            continue
        if k.startswith('ACTION'):
            continue

        yield (k, k, "", i)


def on_shortcut_update(self, context):
    unregister_shortcut("mesh.just_delete")
    register_shortcut("mesh.just_delete")


class JustDeletePrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    multi_policy: bpy.props.EnumProperty(
        name="Multi-component select preference",
        items=[
        ("VEF", "Vertices, then Edges, then Faces", "", 1),
        ("FEV", "Faces, then Edges, then Vertices", "", 2),
        ],
        description="Order preference in case of multi-component selection",
        default='FEV'
    )

    del_shortcut: bpy.props.EnumProperty(
        name="Delete Shortcut",
        items=list(get_key_types()),
        default='X',
        update=on_shortcut_update
    )

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        box = column.box()
        col = box.column()

        col.prop(self, "multi_policy")
        col.prop(self, "del_shortcut")





def register_shortcut(id_name):
    prefs = bpy.context.preferences.addons[__package__].preferences

    # mostly to get the keymap working
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Mesh")
        kmi = km.keymap_items.new(id_name, prefs.del_shortcut, 'PRESS')


def unregister_shortcut(id_name):
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.get('Mesh')
        if km is not None:
            for kmi in km.keymap_items:
                if kmi.idname == id_name:
                    km.keymap_items.remove(kmi)


def register_classes():
    bpy.utils.register_class(JustDeletePrefs)


def unregister_classes():
    bpy.utils.unregister_class(JustDeletePrefs)
