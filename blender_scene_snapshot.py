# Blender Scene Snapshot - Copy this into Blender Text Editor
# This will give you a detailed "screenshot" of your scene in text format

import bpy
import json

def scene_snapshot():
    """Create a detailed snapshot of the current Blender scene"""
    
    print("📸 BLENDER SCENE SNAPSHOT")
    print("=" * 50)
    
    scene = bpy.context.scene
    
    # Basic scene info
    print(f"🎬 Scene: {scene.name}")
    print(f"📊 Frame: {scene.frame_current} / {scene.frame_start}-{scene.frame_end}")
    print(f"🎯 Objects: {len(scene.objects)}")
    print()
    
    # Active object details
    if bpy.context.active_object:
        obj = bpy.context.active_object
        print(f"🎯 ACTIVE OBJECT: {obj.name}")
        print(f"   Type: {obj.type}")
        print(f"   Location: ({obj.location.x:.2f}, {obj.location.y:.2f}, {obj.location.z:.2f})")
        print(f"   Visible: {obj.visible_get()}")
        
        # Shape key info
        if obj.type == 'MESH' and obj.data.shape_keys:
            shape_keys = obj.data.shape_keys.key_blocks
            print(f"   Shape Keys: {len(shape_keys)}")
            
            # Show active shape keys
            active_keys = []
            for key in shape_keys:
                if key.value > 0:
                    active_keys.append(f"{key.name}({key.value:.2f})")
            
            if active_keys:
                print(f"   Active Keys: {', '.join(active_keys)}")
            else:
                print(f"   Active Keys: None (neutral face)")
        else:
            print(f"   Shape Keys: None")
        print()
    
    # Selected objects
    selected = bpy.context.selected_objects
    if selected:
        print(f"✅ SELECTED OBJECTS ({len(selected)}):")
        for obj in selected:
            print(f"   • {obj.name} ({obj.type})")
        print()
    
    # All objects summary
    print("📋 ALL OBJECTS:")
    for obj in scene.objects:
        status = "🎯" if obj == bpy.context.active_object else "📦"
        visible = "👁️" if obj.visible_get() else "🙈"
        selected = "✅" if obj.select_get() else "⚪"
        
        print(f"   {status} {visible} {selected} {obj.name} ({obj.type})")
        
        # Add shape key info for meshes
        if obj.type == 'MESH' and obj.data.shape_keys:
            keys = obj.data.shape_keys.key_blocks
            active_count = sum(1 for key in keys if key.value > 0)
            print(f"      🎭 Shape Keys: {len(keys)} total, {active_count} active")
    
    print()
    
    # Materials
    if bpy.data.materials:
        print("🎨 MATERIALS:")
        for mat in bpy.data.materials:
            print(f"   • {mat.name}")
    
    # Cameras
    cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
    if cameras:
        print("\n📷 CAMERAS:")
        for cam in cameras:
            print(f"   • {cam.name}: {cam.data.type} (Lens: {cam.data.lens}mm)")
    
    # Lights
    lights = [obj for obj in scene.objects if obj.type == 'LIGHT']
    if lights:
        print("\n💡 LIGHTS:")
        for light in lights:
            print(f"   • {light.name}: {light.data.type} (Energy: {light.data.energy})")
    
    print("\n🎯 FACE OBJECT IDENTIFICATION:")
    face_objects = []
    for obj in scene.objects:
        if obj.type == 'MESH' and obj.data.shape_keys:
            # Check if it might be a face (has many shape keys)
            key_count = len(obj.data.shape_keys.key_blocks)
            if key_count > 5:  # Likely a face if it has many shape keys
                face_objects.append((obj.name, key_count))
    
    if face_objects:
        print("   Potential face objects:")
        for name, count in face_objects:
            print(f"   • {name}: {count} shape keys")
    else:
        print("   No obvious face objects found")
    
    print("\n💡 TO RESET FACE SHAPE KEYS:")
    print("   1. Select your face object")
    print("   2. Run the shape key reset script")
    print("   3. Or use: [shape key reset code here]")

# Run the snapshot
scene_snapshot()