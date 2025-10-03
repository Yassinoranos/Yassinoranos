# Blender 3.6 Face Shape Key Reset - Targeted Version
# Modify the OBJECT_NAME variable below to match your face object

import bpy

# ⚠️ CHANGE THIS TO YOUR FACE OBJECT NAME ⚠️
OBJECT_NAME = "Face"  # Replace "Face" with your actual face object name

def reset_face_shape_keys_by_name(object_name):
    """Reset all shape keys on a specific object by name"""
    
    # Find the object
    if object_name not in bpy.data.objects:
        print(f"❌ Object '{object_name}' not found")
        print("Available objects:")
        for obj in bpy.data.objects:
            print(f"  • {obj.name}")
        return
    
    obj = bpy.data.objects[object_name]
    
    if obj.type != 'MESH':
        print(f"❌ '{object_name}' is not a mesh")
        return
    
    if not obj.data.shape_keys:
        print(f"❌ '{object_name}' has no shape keys")
        return
    
    print(f"🎭 Resetting shape keys on '{object_name}'...")
    
    # Select and make active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Reset all shape keys to 0
    shape_keys = obj.data.shape_keys
    reset_count = 0
    
    for key_block in shape_keys.key_blocks:
        if key_block.name != "Basis":  # Skip the basis shape
            old_value = key_block.value
            key_block.value = 0.0
            reset_count += 1
            print(f"  • {key_block.name}: {old_value:.3f} → 0.000")
    
    # Update the mesh
    obj.data.update()
    
    print(f"✅ Reset {reset_count} shape keys on '{object_name}'!")
    print("🎭 Face is now in neutral expression!")

# Run the function with the specified object name
reset_face_shape_keys_by_name(OBJECT_NAME)