#!/usr/bin/env python3
"""
Blender Scene Capture Script
This script will capture detailed information about your Blender scene
"""

import bpy
import json
from mathutils import Vector

def capture_scene_info():
    """Capture comprehensive scene information"""
    
    print("📸 CAPTURING BLENDER SCENE INFORMATION")
    print("=" * 60)
    
    scene = bpy.context.scene
    scene_info = {
        "scene_name": scene.name,
        "frame_start": scene.frame_start,
        "frame_end": scene.frame_end,
        "frame_current": scene.frame_current,
        "objects": [],
        "materials": [],
        "lights": [],
        "cameras": [],
        "meshes": [],
        "active_object": None,
        "selected_objects": []
    }
    
    # Get active object info
    if bpy.context.active_object:
        active_obj = bpy.context.active_object
        scene_info["active_object"] = {
            "name": active_obj.name,
            "type": active_obj.type,
            "location": list(active_obj.location),
            "rotation": list(active_obj.rotation_euler),
            "scale": list(active_obj.scale),
            "visible": active_obj.visible_get(),
            "has_shape_keys": bool(active_obj.data.shape_keys) if active_obj.type == 'MESH' else False
        }
        
        # Get shape key details if available
        if active_obj.type == 'MESH' and active_obj.data.shape_keys:
            shape_keys_info = []
            for key_block in active_obj.data.shape_keys.key_blocks:
                shape_keys_info.append({
                    "name": key_block.name,
                    "value": key_block.value,
                    "relative_key": key_block.relative_key.name if key_block.relative_key else None
                })
            scene_info["active_object"]["shape_keys"] = shape_keys_info
    
    # Get selected objects
    for obj in bpy.context.selected_objects:
        scene_info["selected_objects"].append({
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location)
        })
    
    # Get all objects
    for obj in scene.objects:
        obj_info = {
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale),
            "visible": obj.visible_get(),
            "selected": obj.select_get()
        }
        
        # Add mesh-specific info
        if obj.type == 'MESH':
            obj_info["vertices"] = len(obj.data.vertices)
            obj_info["faces"] = len(obj.data.polygons)
            obj_info["edges"] = len(obj.data.edges)
            obj_info["has_shape_keys"] = bool(obj.data.shape_keys)
            
            # Get shape key summary
            if obj.data.shape_keys:
                shape_keys = obj.data.shape_keys.key_blocks
                obj_info["shape_keys_count"] = len(shape_keys)
                obj_info["shape_keys_active"] = [key.name for key in shape_keys if key.value > 0]
        
        # Add camera-specific info
        elif obj.type == 'CAMERA':
            obj_info["camera_type"] = obj.data.type
            obj_info["lens"] = obj.data.lens
            obj_info["fov"] = obj.data.angle
        
        # Add light-specific info
        elif obj.type == 'LIGHT':
            obj_info["light_type"] = obj.data.type
            obj_info["energy"] = obj.data.energy
            obj_info["color"] = list(obj.data.color)
        
        scene_info["objects"].append(obj_info)
    
    # Get materials
    for mat in bpy.data.materials:
        scene_info["materials"].append({
            "name": mat.name,
            "use_nodes": mat.use_nodes,
            "use_transparency": mat.use_transparency
        })
    
    # Get lights
    for light in bpy.data.lights:
        scene_info["lights"].append({
            "name": light.name,
            "type": light.type,
            "energy": light.energy,
            "color": list(light.color)
        })
    
    # Get cameras
    for camera in bpy.data.cameras:
        scene_info["cameras"].append({
            "name": camera.name,
            "type": camera.type,
            "lens": camera.lens,
            "fov": camera.angle
        })
    
    # Get meshes
    for mesh in bpy.data.meshes:
        scene_info["meshes"].append({
            "name": mesh.name,
            "vertices": len(mesh.vertices),
            "faces": len(mesh.polygons),
            "edges": len(mesh.edges),
            "has_shape_keys": bool(mesh.shape_keys)
        })
    
    return scene_info

def print_scene_summary(scene_info):
    """Print a formatted summary of the scene"""
    
    print(f"\n📋 SCENE SUMMARY: {scene_info['scene_name']}")
    print("=" * 50)
    
    print(f"🎬 Frame Range: {scene_info['frame_start']} - {scene_info['frame_end']} (Current: {scene_info['frame_current']})")
    print(f"📊 Total Objects: {len(scene_info['objects'])}")
    print(f"🎨 Materials: {len(scene_info['materials'])}")
    print(f"💡 Lights: {len(scene_info['lights'])}")
    print(f"📷 Cameras: {len(scene_info['cameras'])}")
    print(f"🔧 Meshes: {len(scene_info['meshes'])}")
    
    # Active object details
    if scene_info['active_object']:
        active = scene_info['active_object']
        print(f"\n🎯 ACTIVE OBJECT: {active['name']}")
        print(f"   Type: {active['type']}")
        print(f"   Location: {active['location']}")
        print(f"   Visible: {active['visible']}")
        
        if active['has_shape_keys'] and 'shape_keys' in active:
            print(f"   Shape Keys: {len(active['shape_keys'])}")
            active_keys = [key['name'] for key in active['shape_keys'] if key['value'] > 0]
            if active_keys:
                print(f"   Active Shape Keys: {', '.join(active_keys)}")
            else:
                print(f"   Active Shape Keys: None (all neutral)")
    
    # Selected objects
    if scene_info['selected_objects']:
        print(f"\n✅ SELECTED OBJECTS ({len(scene_info['selected_objects'])}):")
        for obj in scene_info['selected_objects']:
            print(f"   • {obj['name']} ({obj['type']})")
    
    # Objects with shape keys
    objects_with_shape_keys = [obj for obj in scene_info['objects'] if obj.get('has_shape_keys', False)]
    if objects_with_shape_keys:
        print(f"\n🎭 OBJECTS WITH SHAPE KEYS ({len(objects_with_shape_keys)}):")
        for obj in objects_with_shape_keys:
            print(f"   • {obj['name']}: {obj.get('shape_keys_count', 0)} keys")
            if obj.get('shape_keys_active'):
                print(f"     Active: {', '.join(obj['shape_keys_active'])}")
    
    # Camera info
    if scene_info['cameras']:
        print(f"\n📷 CAMERAS:")
        for cam in scene_info['cameras']:
            print(f"   • {cam['name']}: {cam['type']} (Lens: {cam['lens']}mm)")
    
    # Light info
    if scene_info['lights']:
        print(f"\n💡 LIGHTS:")
        for light in scene_info['lights']:
            print(f"   • {light['name']}: {light['type']} (Energy: {light['energy']})")

def save_scene_data(scene_info, filename="blender_scene_data.json"):
    """Save scene data to JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(scene_info, f, indent=2)
        print(f"\n💾 Scene data saved to: {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Error saving scene data: {e}")
        return False

def main():
    """Main function to capture and display scene information"""
    
    print("📸 BLENDER SCENE CAPTURE TOOL")
    print("=" * 40)
    
    # Capture scene information
    scene_info = capture_scene_info()
    
    # Print summary
    print_scene_summary(scene_info)
    
    # Save to file
    save_scene_data(scene_info)
    
    # Return the data for potential use
    return scene_info

# Run the capture
if __name__ == "__main__":
    scene_data = main()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Review the scene summary above")
    print("2. Check the saved JSON file for detailed data")
    print("3. Use this information to identify your face object")
    print("4. Run the shape key reset script on the correct object")