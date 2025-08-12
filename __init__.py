bl_info = {
    "name": "LODGen",
    "description": "Generate LODs for Games in 3 Clicks or Less",
    "author": "F1dg3t",
    "version": (0, 0, 5),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Create Tab > LODGen",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import importlib
from . import main

importlib.reload(main)

def register():
    main.register()

def unregister():
    main.unregister()

if __name__ == "__main__":
    register()
