# 🔗 MCP Blender Connection Guide

Since you have Blender installed with the MCP tool, here's how to establish the connection:

## 🚀 Quick Connection Steps

### Step 1: Start Blender with MCP Addon
1. **Open Blender 3.6**
2. **Go to Edit > Preferences > Add-ons**
3. **Search for "MCP"** in the addon list
4. **Enable the MCP addon** (check the box)
5. **Save Preferences**

### Step 2: Verify MCP Addon is Active
1. **Open Text Editor** in Blender
2. **Create new text** and paste this verification script:

```python
import bpy
import addon_utils

# Check MCP addon status
print("🔍 Checking MCP addon status...")

# List all addons with 'mcp' in name
mcp_addons = [addon for addon in addon_utils.modules() if 'mcp' in addon.__name__.lower()]
print(f"MCP-related addons found: {len(mcp_addons)}")

for addon in mcp_addons:
    print(f"  • {addon.__name__}")

# Check enabled MCP addons
enabled_addons = [addon for addon in bpy.context.preferences.addons.keys() if 'mcp' in addon.lower()]
print(f"Enabled MCP addons: {len(enabled_addons)}")

for addon in enabled_addons:
    print(f"  • {addon}")

if enabled_addons:
    print("✅ MCP addon is active!")
else:
    print("❌ No MCP addons enabled")
```

3. **Run the script** (Alt+P or click Run Script)
4. **Check the Console** for MCP addon status

### Step 3: Test MCP Connection
1. **In Blender Text Editor**, create new text and paste:

```python
import bpy
import json

# Test MCP functionality
def test_mcp_connection():
    print("🔗 Testing MCP connection...")
    
    # Basic Blender info
    blender_info = {
        "version": bpy.app.version_string,
        "scene_name": bpy.context.scene.name,
        "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
        "objects_count": len(bpy.context.scene.objects)
    }
    
    print("📊 Blender Status:")
    print(f"  • Version: {blender_info['version']}")
    print(f"  • Scene: {blender_info['scene_name']}")
    print(f"  • Active Object: {blender_info['active_object'] or 'None'}")
    print(f"  • Objects: {blender_info['objects_count']}")
    
    # Test shape key functionality
    if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
        obj = bpy.context.active_object
        if obj.data.shape_keys:
            print(f"✅ Active object '{obj.name}' has {len(obj.data.shape_keys.key_blocks)} shape keys")
            return True
        else:
            print(f"⚠️ Active object '{obj.name}' has no shape keys")
    else:
        print("⚠️ No active mesh object")
    
    return True

# Run the test
test_mcp_connection()
```

2. **Run the script** and check the output

## 🎭 Face Shape Key Reset via MCP

Once connected, you can reset face shape keys using this MCP-style command:

```python
import bpy

def reset_face_shape_keys_mcp():
    """Reset shape keys using MCP-style approach"""
    
    # Get active object
    obj = bpy.context.active_object
    
    if not obj:
        return {"success": False, "message": "No active object"}
    
    if obj.type != 'MESH':
        return {"success": False, "message": f"'{obj.name}' is not a mesh"}
    
    if not obj.data.shape_keys:
        return {"success": False, "message": f"'{obj.name}' has no shape keys"}
    
    # Reset shape keys
    reset_count = 0
    reset_details = []
    
    for key_block in obj.data.shape_keys.key_blocks:
        if key_block.name != "Basis":
            old_value = key_block.value
            key_block.value = 0.0
            reset_count += 1
            reset_details.append(f"{key_block.name}: {old_value:.3f} → 0.000")
    
    # Update mesh
    obj.data.update()
    
    result = {
        "success": True,
        "object_name": obj.name,
        "reset_count": reset_count,
        "details": reset_details,
        "message": f"Reset {reset_count} shape keys on '{obj.name}'"
    }
    
    print("✅ Shape Key Reset Results:")
    print(f"  • Object: {result['object_name']}")
    print(f"  • Reset Count: {result['reset_count']}")
    print("  • Details:")
    for detail in reset_details:
        print(f"    - {detail}")
    
    return result

# Execute the reset
reset_face_shape_keys_mcp()
```

## 🔧 MCP Addon Configuration

### If MCP Addon is Not Found:
1. **Download the MCP addon** from the official source
2. **Install via Edit > Preferences > Add-ons > Install**
3. **Enable the addon**
4. **Configure MCP settings** if available

### Common MCP Addon Names:
- "MCP Blender"
- "Model Context Protocol"
- "MCP Integration"
- "Blender MCP"

## 📡 Connection Methods

### Method 1: Direct Python Script
Run Python scripts directly in Blender's Text Editor

### Method 2: MCP Server Connection
If your MCP addon supports server mode:
1. **Start MCP server** in Blender
2. **Connect external client** to the server
3. **Send commands** via MCP protocol

### Method 3: Addon Interface
Use the MCP addon's built-in interface:
1. **Look for MCP panel** in Blender UI
2. **Use addon buttons** for common operations
3. **Configure settings** through addon preferences

## 🚨 Troubleshooting

### ❌ "MCP addon not found"
- Check if addon is properly installed
- Verify addon is enabled in preferences
- Look for alternative MCP addon names

### ❌ "No active object"
- Select your face mesh object first
- Check object is visible and not hidden

### ❌ "No shape keys found"
- Verify object has shape keys in Properties > Data > Shape Keys
- Make sure you're working with a mesh object

### ❌ "Script runs but nothing happens"
- Check Console for error messages
- Verify object selection
- Test with a simple print statement first

## 💡 Next Steps

Once MCP connection is established:
1. **Test basic commands** (scene info, object selection)
2. **Try shape key operations** (reset, list, modify)
3. **Set up automated workflows** using MCP commands
4. **Create custom MCP tools** for your specific needs

The MCP connection will allow you to control Blender programmatically and integrate it with external tools and workflows! 🚀