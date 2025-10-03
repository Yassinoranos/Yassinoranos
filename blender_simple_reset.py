# Blender 3.6 Face Shape Key Reset - Simple Version
# Copy and paste this into Blender's Text Editor and run it

import bpy

def reset_face_shape_keys():
    """Reset all shape keys on the active object to neutral"""
    
    # Get the active object
    obj = bpy.context.active_object
    
    if not obj:
        print("❌ No active object selected")
        return
    
    if obj.type != 'MESH':
        print(f"❌ '{obj.name}' is not a mesh")
        return
    
    if not obj.data.shape_keys:
        print(f"❌ '{obj.name}' has no shape keys")
        return
    
    print(f"🎭 Resetting shape keys on '{obj.name}'...")
    
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
    
    print(f"✅ Reset {reset_count} shape keys!")
    print("🎭 Face is now in neutral expression!")

# Run the function
reset_face_shape_keys()