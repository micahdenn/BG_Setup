import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

bl_info = {
    "name": "BG Setup",
    "author": "Micah Denn",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "Properties > Scene > BG Setup",
    "description": "Quickly set scene, camera and file output names.",
    #"doc_url": "",
    "category": "RND",
    }

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):

    my_int: IntProperty(
        name = "Episode Number",
        description="0-999",
        default = 1,
        min = 0,
        max = 999
        )
    my_string: StringProperty(
        name='suffix'
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_HelloWorld(Operator):
    """Sets scene, camera and file output names"""
    bl_label = "Set Names"
    bl_idname = "wm.hello_world"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Hello World")
        print("int value:", mytool.my_int)
        scene_name = bpy.context.window.scene.name
        rnd, location_name = scene_name.split("_",1)
        location_name =''.join(location_name)
        episode = "RND{:03d}_{}{}".format(mytool.my_int,location_name,mytool.my_string)
        bpy.context.window.scene.name = episode
        
        camera = bpy.context.scene.camera.name
        bpy.data.objects[camera].name = episode + str("_camera")
        
        bpy.context.scene.render.filepath = episode
        bpy.context.scene.node_tree.nodes["File Output"].base_path = episode
        

        return {'FINISHED'}

    
class WM_OT_remove(Operator):
    """Sets scene, camera and file output names"""
    bl_label = "Remove Sufxix"
    bl_idname = "wm.remove"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print("Hello World")
        print("int value:", mytool.my_int)
        scene_name = bpy.context.window.scene.name
        rnd, location_name = scene_name.rsplit("_",1)
        location_name =''.join(location_name)
        episode = "{}".format(rnd)
        if len(episode)>6:
            bpy.context.window.scene.name = episode
            
            camera = bpy.context.scene.camera.name
            bpy.data.objects[camera].name = episode + str("_camera")
            
            bpy.context.scene.render.filepath = episode
            bpy.context.scene.node_tree.nodes["File Output"].base_path = episode
        else:
            pass

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class OBJECT_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "Royals Next Door - File Setup Addon"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = "PROPERTIES"   
    bl_region_type = "WINDOW"
    bl_context = "scene"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "my_int")
        layout.prop(mytool, "my_string")
        layout.separator()
        layout.operator("wm.hello_world")
        layout.operator("wm.remove")
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_HelloWorld,
    WM_OT_remove,
    OBJECT_MT_CustomMenu,
    OBJECT_PT_CustomPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
