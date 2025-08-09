import bpy
import re
from bpy.props import (
    FloatProperty,
    IntProperty,
    CollectionProperty,
    StringProperty,
    PointerProperty
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
    UIList
)

# -------------------
# Property Storage
# -------------------

class LODGenObject(PropertyGroup):
    name: StringProperty(name="Object Name")

class LODGenProperties(PropertyGroup):
    objects: CollectionProperty(type=LODGenObject)
    decimation_scale: FloatProperty(
        name="Decimation Scale",
        description="Scale for decimation modifier (1.0 = no change, 0.5 = half)",
        default=0.5,
        min=0.0,
        max=1.0
    )
    iterations: IntProperty(
        name="Iterations",
        description="Number of LODs to generate",
        default=6,
        min=1
    )

# -------------------
# UI List
# -------------------

class LODGEN_UL_ObjectList(UIList):
    def draw_item(
        self, context, layout, data, item, icon,
        active_data, active_propname, index
    ):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon='MESH_DATA')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="")

# -------------------
# Operators
# -------------------

class LODGEN_OT_AddSelected(Operator):
    bl_idname = "lodgen.add_selected"
    bl_label = "Add Selected Objects"
    bl_description = "Add currently selected objects to LOD list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.lodgen_props
        for obj in context.selected_objects:
            if obj.name not in [o.name for o in props.objects]:
                item = props.objects.add()
                item.name = obj.name
        return {'FINISHED'}

class LODGEN_OT_RemoveSelected(Operator):
    bl_idname = "lodgen.remove_selected"
    bl_label = "Remove Selected From List"
    bl_description = "Remove selected entries from the LOD list"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        props = context.scene.lodgen_props
        return props.objects and len(props.objects) > 0

    def execute(self, context):
        props = context.scene.lodgen_props
        selected_indices = [i for i, item in enumerate(props.objects) if item.name == props.objects[context.scene.lodgen_list_index].name]
        if selected_indices:
            props.objects.remove(selected_indices[0])
        return {'FINISHED'}

class LODGEN_OT_GenerateLODs(Operator):
    bl_idname = "lodgen.generate_lods"
    bl_label = "Generate LODs"
    bl_description = "Generate LOD meshes for all objects in the list"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.lodgen_props
        step_scale = props.decimation_scale  # per-step multiplier
        iterations = props.iterations

        for entry in props.objects:
            original_obj = bpy.data.objects.get(entry.name)
            if not original_obj:
                self.report({'WARNING'}, f"Object {entry.name} not found, skipping.")
                continue

            base_name = re.sub(r"\.\d+$", "", original_obj.name)
            lod_collection_name = f"{base_name}_LODs"

            # Get or create LOD collection
            if lod_collection_name in bpy.data.collections:
                target_collection = bpy.data.collections[lod_collection_name]
                # Remove old LODs but leave the original
                for o in list(target_collection.objects):
                    bpy.data.objects.remove(o, do_unlink=True)
            else:
                target_collection = bpy.data.collections.new(lod_collection_name)
                context.scene.collection.children.link(target_collection)

            # Hide the original but do not move it
            original_obj.hide_set(True)
            original_obj.hide_render = True

            # Create LOD0 from the original
            lod0_obj = original_obj.copy()
            lod0_obj.data = original_obj.data.copy()
            lod0_obj.name = f"{base_name}_LOD0"
            target_collection.objects.link(lod0_obj)

            # Apply all modifiers on LOD0
            bpy.context.view_layer.objects.active = lod0_obj
            for mod in list(lod0_obj.modifiers):
                bpy.ops.object.modifier_apply(modifier=mod.name)

            current_obj = lod0_obj
            current_ratio = step_scale

            # Create further LODs progressively
            for lod_level in range(1, iterations):
                new_obj = current_obj.copy()
                new_obj.data = current_obj.data.copy()
                new_obj.name = f"{base_name}_LOD{lod_level}"
                target_collection.objects.link(new_obj)

                # Add decimate modifier
                dec_mod = new_obj.modifiers.new(name="LODGen_Decimate", type='DECIMATE')
                dec_mod.ratio = current_ratio

                bpy.context.view_layer.objects.active = new_obj
                bpy.ops.object.modifier_apply(modifier=dec_mod.name)

                # Prepare for next iteration
                current_obj = new_obj
                current_ratio *= step_scale

        self.report({'INFO'}, "LOD generation complete.")
        return {'FINISHED'}

# -------------------
# UI Panel
# -------------------

class LODGEN_PT_MainPanel(Panel):
    bl_label = "LODGen"
    bl_idname = "LODGEN_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Create'

    def draw(self, context):
        layout = self.layout
        props = context.scene.lodgen_props

        row = layout.row()
        row.template_list("LODGEN_UL_ObjectList", "", props, "objects", context.scene, "lodgen_list_index")

        col = row.column(align=True)
        col.operator("lodgen.add_selected", icon='ADD', text="")
        col.operator("lodgen.remove_selected", icon='REMOVE', text="")

        layout.prop(props, "decimation_scale")
        layout.prop(props, "iterations")
        layout.operator("lodgen.generate_lods", icon='MOD_DECIM')


# -------------------
# Registration
# -------------------

classes = (
    LODGenObject,
    LODGenProperties,
    LODGEN_UL_ObjectList,
    LODGEN_OT_AddSelected,
    LODGEN_OT_RemoveSelected,
    LODGEN_OT_GenerateLODs,
    LODGEN_PT_MainPanel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.lodgen_props = PointerProperty(type=LODGenProperties)
    bpy.types.Scene.lodgen_list_index = IntProperty(default=0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.lodgen_props
    del bpy.types.Scene.lodgen_list_index
