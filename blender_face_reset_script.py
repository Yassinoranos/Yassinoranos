#!/usr/bin/env python3
"""
Blender 3.6 Face Shape Key Reset Script
Run this directly in Blender 3.6 to reset shape keys on human face
"""

import bpy
import bmesh
from mathutils import Vector

def reset_face_shape_keys(object_name="", reset_to_basis=True):
    """
    Reset shape keys on human face mesh object
    
    Args:
        object_name (str): Name of the face object (optional, uses active object if empty)
        reset_to_basis (bool): Reset all shape keys to basis (0) value
    """
    
    print("🎭 Starting Face Shape Key Reset...")
    print("=" * 50)
    
    # Select the object
    if object_name:
        if object_name in bpy.data.objects:
            obj = bpy.data.objects[object_name]
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            print(f"✅ Selected object: {obj.name}")
        else:
            print(f"❌ Object '{object_name}' not found")
            return False
    else:
        # Use active object
        obj = bpy.context.active_object
        if not obj:
            print("❌ No active object selected")
            return False
        print(f"✅ Using active object: {obj.name}")
    
    # Check if it's a mesh
    if obj.type != 'MESH':
        print(f"❌ Object '{obj.name}' is not a mesh")
        return False
    
    # Check if it has shape keys
    if not obj.data.shape_keys:
        print(f"❌ Object '{obj.name}' has no shape keys")
        return False
    
    print(f"✅ Found shape keys on '{obj.name}'")
    
    # Get shape keys
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    
    print(f"📊 Total shape keys found: {len(key_blocks)}")
    
    # Reset all shape keys
    reset_count = 0
    reset_list = []
    
    for key_block in key_blocks:
        if key_block.name != "Basis":  # Don't reset the basis shape
            old_value = key_block.value
            key_block.value = 0.0  # Reset to basis
            reset_count += 1
            reset_list.append(f"  • {key_block.name}: {old_value:.3f} → 0.000")
    
    print(f"🔄 Reset {reset_count} shape keys:")
    for item in reset_list:
        print(item)
    
    # Update the mesh
    obj.data.update()
    
    # Force viewport update
    bpy.context.view_layer.update()
    
    print(f"✅ Successfully reset {reset_count} shape keys on '{obj.name}'")
    print("🎭 Face should now be in neutral expression!")
    
    return True

def list_shape_keys(object_name=""):
    """
    List all shape keys on the face object
    """
    print("📋 Listing Shape Keys...")
    print("=" * 30)
    
    # Select the object
    if object_name:
        if object_name in bpy.data.objects:
            obj = bpy.data.objects[object_name]
        else:
            print(f"❌ Object '{object_name}' not found")
            return
    else:
        obj = bpy.context.active_object
        if not obj:
            print("❌ No active object selected")
            return
    
    if obj.type != 'MESH':
        print(f"❌ Object '{obj.name}' is not a mesh")
        return
    
    if not obj.data.shape_keys:
        print(f"❌ Object '{obj.name}' has no shape keys")
        return
    
    shape_keys = obj.data.shape_keys
    key_blocks = shape_keys.key_blocks
    
    print(f"📊 Shape Keys on '{obj.name}':")
    for i, key_block in enumerate(key_blocks):
        status = "🔵" if key_block.value > 0 else "⚪"
        print(f"  {i+1:2d}. {status} {key_block.name}: {key_block.value:.3f}")

def main():
    """
    Main function - you can modify this to target specific objects
    """
    print("🎭 Blender 3.6 Face Shape Key Reset Tool")
    print("=" * 60)
    print()
    
    # Option 1: Reset active object (recommended)
    print("Option 1: Reset active object")
    success = reset_face_shape_keys("", True)
    
    if success:
        print()
        print("📋 Current shape key values:")
        list_shape_keys("")
    
    print()
    print("💡 To reset a specific object, modify the script:")
    print("   reset_face_shape_keys('YourFaceObjectName', True)")
    print()
    print("💡 To list shape keys on a specific object:")
    print("   list_shape_keys('YourFaceObjectName')")

# Run the main function
if __name__ == "__main__":
    main()

# Alternative: Direct execution functions
# Uncomment and modify these lines to target specific objects:

# Reset specific face object (replace 'Face' with your object name):
# reset_face_shape_keys('Face', True)

# List shape keys on specific object:
# list_shape_keys('Face')

# Reset active object:
# reset_face_shape_keys('', True)