# 🎭 Blender 3.6 Face Shape Key Reset Guide

## Quick Start (3 Methods)

### Method 1: Simple Active Object Reset
1. **Select your face object** in Blender
2. **Open Text Editor** (Scripting workspace or Window > Text Editor)
3. **Create new text** (Text > New)
4. **Copy and paste** the contents of `blender_simple_reset.py`
5. **Click "Run Script"** button or press Alt+P

### Method 2: Targeted Object Reset
1. **Open Text Editor** in Blender
2. **Create new text**
3. **Copy and paste** the contents of `blender_targeted_reset.py`
4. **Edit the OBJECT_NAME variable** at the top:
   ```python
   OBJECT_NAME = "YourFaceObjectName"  # Change this!
   ```
5. **Click "Run Script"**

### Method 3: Full Featured Script
1. **Open Text Editor** in Blender
2. **Create new text**
3. **Copy and paste** the contents of `blender_face_reset_script.py`
4. **Click "Run Script"**

## What Each Script Does

### Simple Reset (`blender_simple_reset.py`)
- ✅ Resets shape keys on **active object**
- ✅ Shows reset progress
- ✅ Perfect for quick resets

### Targeted Reset (`blender_targeted_reset.py`)
- ✅ Resets shape keys on **specific object by name**
- ✅ Lists available objects if target not found
- ✅ Perfect when you know the object name

### Full Featured (`blender_face_reset_script.py`)
- ✅ Multiple functions available
- ✅ List shape keys before/after
- ✅ Detailed progress reporting
- ✅ Error handling

## Usage Examples

### Example 1: Reset Active Face Object
```python
# Select your face object first, then run:
import bpy

obj = bpy.context.active_object
if obj.data.shape_keys:
    for key_block in obj.data.shape_keys.key_blocks:
        if key_block.name != "Basis":
            key_block.value = 0.0
    obj.data.update()
    print("✅ Face reset to neutral!")
```

### Example 2: Reset Specific Face Object
```python
# Replace "Face" with your actual object name:
import bpy

face_obj = bpy.data.objects["Face"]  # Change "Face" to your object name
if face_obj.data.shape_keys:
    for key_block in face_obj.data.shape_keys.key_blocks:
        if key_block.name != "Basis":
            key_block.value = 0.0
    face_obj.data.update()
    print("✅ Face reset to neutral!")
```

## Troubleshooting

### ❌ "No active object selected"
**Solution**: Select your face object first, then run the script

### ❌ "Object 'Face' not found"
**Solution**: 
1. Check the object name in the Outliner
2. Update the OBJECT_NAME variable in the script
3. Or use the simple reset method with active object

### ❌ "Object has no shape keys"
**Solution**: 
1. Make sure your face object has shape keys
2. Check in Properties > Data > Shape Keys
3. If no shape keys exist, you need to add them first

### ❌ Script runs but nothing happens
**Solution**:
1. Check the Console (Window > Toggle System Console)
2. Look for error messages
3. Make sure the object is a mesh with shape keys

## Advanced Usage

### List All Shape Keys Before Reset
```python
import bpy

obj = bpy.context.active_object
if obj.data.shape_keys:
    print("Current shape key values:")
    for key_block in obj.data.shape_keys.key_blocks:
        print(f"  {key_block.name}: {key_block.value:.3f}")
```

### Reset Only Specific Shape Keys
```python
import bpy

obj = bpy.context.active_object
if obj.data.shape_keys:
    # Reset only eye-related shape keys
    for key_block in obj.data.shape_keys.key_blocks:
        if "Eye" in key_block.name and key_block.name != "Basis":
            key_block.value = 0.0
    obj.data.update()
```

### Save Script as Addon
1. Save the script as `face_reset.py`
2. Go to Edit > Preferences > Add-ons
3. Click "Install" and select the script
4. Enable the addon
5. Access via Search menu (F3) or add to custom menu

## Tips for Blender 3.6

- ✅ **Always select the face object** before running scripts
- ✅ **Check the Console** for output messages
- ✅ **Use Text Editor** for running Python scripts
- ✅ **Save scripts** for future use
- ✅ **Test on a copy** of your scene first

## Common Face Object Names
- "Face"
- "Head"
- "Character"
- "Human"
- "Mesh"
- "Body"

Check your Outliner to see the exact name!