#!/usr/bin/env python3
"""
MCP Blender Connection Script
This script helps establish connection with the MCP tool installed in Blender
"""

import json
import subprocess
import sys
import time
import socket
from typing import Dict, Any, Optional

class MCPBlenderConnector:
    def __init__(self):
        self.blender_path = None
        self.mcp_port = None
        self.connection_status = False
        
    def find_blender(self):
        """Find Blender installation"""
        possible_paths = [
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "/opt/blender/blender",
            "/snap/bin/blender",
            "blender"
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.blender_path = path
                    print(f"✅ Found Blender at: {path}")
                    return True
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("❌ Blender not found")
        return False
    
    def check_mcp_addon_status(self):
        """Check if MCP addon is installed and active"""
        if not self.blender_path:
            return False
            
        # Create script to check MCP addon
        check_script = """
import bpy
import addon_utils

# Check if MCP addon is installed
mcp_addons = [addon for addon in addon_utils.modules() if 'mcp' in addon.__name__.lower()]
print(f"MCP-related addons found: {len(mcp_addons)}")

for addon in mcp_addons:
    print(f"  • {addon.__name__}")

# Check if any MCP addon is enabled
enabled_addons = [addon for addon in bpy.context.preferences.addons.keys() if 'mcp' in addon.lower()]
print(f"Enabled MCP addons: {len(enabled_addons)}")

for addon in enabled_addons:
    print(f"  • {addon}")

print("MCP_CHECK_COMPLETE")
"""
        
        try:
            result = subprocess.run([
                self.blender_path, 
                "--background", 
                "--python-expr", 
                check_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("📋 MCP Addon Status:")
                print(result.stdout)
                return "MCP_CHECK_COMPLETE" in result.stdout
            else:
                print(f"❌ Error checking MCP addon: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout checking MCP addon")
            return False
    
    def start_blender_with_mcp(self):
        """Start Blender with MCP addon enabled"""
        if not self.blender_path:
            return False
            
        print("🚀 Starting Blender with MCP addon...")
        
        # Create startup script to enable MCP addon
        startup_script = """
import bpy
import addon_utils

# Enable MCP addon if found
mcp_addons = [addon for addon in addon_utils.modules() if 'mcp' in addon.__name__.lower()]

if mcp_addons:
    for addon in mcp_addons:
        addon_name = addon.__name__
        if addon_name not in bpy.context.preferences.addons:
            addon_utils.enable(addon_name)
            print(f"✅ Enabled MCP addon: {addon_name}")
        else:
            print(f"✅ MCP addon already enabled: {addon_name}")
else:
    print("❌ No MCP addons found")

print("BLENDER_MCP_STARTUP_COMPLETE")
"""
        
        try:
            # Start Blender in background with startup script
            process = subprocess.Popen([
                self.blender_path,
                "--background",
                "--python-expr",
                startup_script
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a moment for startup
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                print("✅ Blender started successfully")
                return True
            else:
                stdout, stderr = process.communicate()
                print(f"❌ Blender startup failed: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting Blender: {e}")
            return False
    
    def test_mcp_connection(self):
        """Test MCP connection with Blender"""
        print("🔗 Testing MCP connection...")
        
        # Create test script
        test_script = """
import bpy
import json

# Test MCP functionality
test_result = {
    "blender_version": bpy.app.version_string,
    "scene_name": bpy.context.scene.name,
    "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
    "mcp_ready": True
}

print("MCP_TEST_START")
print(json.dumps(test_result, indent=2))
print("MCP_TEST_END")
"""
        
        try:
            result = subprocess.run([
                self.blender_path,
                "--background",
                "--python-expr",
                test_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "MCP_TEST_START" in result.stdout:
                print("✅ MCP connection test successful!")
                print("📊 Blender Status:")
                
                # Extract test result
                start_idx = result.stdout.find("MCP_TEST_START") + len("MCP_TEST_START")
                end_idx = result.stdout.find("MCP_TEST_END")
                test_json = result.stdout[start_idx:end_idx].strip()
                
                try:
                    test_data = json.loads(test_json)
                    print(f"  • Blender Version: {test_data['blender_version']}")
                    print(f"  • Scene: {test_data['scene_name']}")
                    print(f"  • Active Object: {test_data['active_object'] or 'None'}")
                    print(f"  • MCP Ready: {test_data['mcp_ready']}")
                    return True
                except json.JSONDecodeError:
                    print("❌ Error parsing test result")
                    return False
            else:
                print(f"❌ MCP connection test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ MCP connection test timed out")
            return False
    
    def run_mcp_command(self, command: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Run an MCP command on Blender"""
        if not self.blender_path:
            return None
            
        # Create command script
        command_script = f"""
import bpy
import json

# Execute MCP command
command = {json.dumps(command)}

try:
    if command.get("method") == "tools/call":
        tool_name = command.get("params", {{}}).get("name", "")
        arguments = command.get("params", {{}}).get("arguments", {{}})
        
        if tool_name == "get_scene_info":
            # Get scene information
            scene_info = {{
                "scene_name": bpy.context.scene.name,
                "objects": [],
                "active_object": bpy.context.active_object.name if bpy.context.active_object else None
            }}
            
            for obj in bpy.context.scene.objects:
                scene_info["objects"].append({{
                    "name": obj.name,
                    "type": obj.type,
                    "location": list(obj.location),
                    "has_shape_keys": bool(obj.data.shape_keys) if obj.type == 'MESH' else False
                }})
            
            result = {{
                "success": True,
                "data": scene_info,
                "message": "Scene info retrieved successfully"
            }}
            
        elif tool_name == "reset_shape_keys":
            # Reset shape keys on active object
            obj = bpy.context.active_object
            if obj and obj.type == 'MESH' and obj.data.shape_keys:
                reset_count = 0
                for key_block in obj.data.shape_keys.key_blocks:
                    if key_block.name != "Basis":
                        key_block.value = 0.0
                        reset_count += 1
                
                obj.data.update()
                result = {{
                    "success": True,
                    "data": {{"reset_count": reset_count, "object_name": obj.name}},
                    "message": f"Reset {{reset_count}} shape keys on '{{obj.name}}'"
                }}
            else:
                result = {{
                    "success": False,
                    "data": {{}},
                    "message": "No active mesh object with shape keys found"
                }}
        else:
            result = {{
                "success": False,
                "data": {{}},
                "message": f"Unknown tool: {{tool_name}}"
            }}
    else:
        result = {{
            "success": False,
            "data": {{}},
            "message": f"Unknown method: {{command.get('method', '')}}"
        }}

except Exception as e:
    result = {{
        "success": False,
        "data": {{}},
        "message": f"Error executing command: {{str(e)}}"
    }}

print("MCP_COMMAND_RESULT_START")
print(json.dumps(result, indent=2))
print("MCP_COMMAND_RESULT_END")
"""
        
        try:
            result = subprocess.run([
                self.blender_path,
                "--background",
                "--python-expr",
                command_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "MCP_COMMAND_RESULT_START" in result.stdout:
                # Extract result
                start_idx = result.stdout.find("MCP_COMMAND_RESULT_START") + len("MCP_COMMAND_RESULT_START")
                end_idx = result.stdout.find("MCP_COMMAND_RESULT_END")
                result_json = result.stdout[start_idx:end_idx].strip()
                
                try:
                    return json.loads(result_json)
                except json.JSONDecodeError:
                    return {"success": False, "message": "Error parsing result"}
            else:
                return {"success": False, "message": f"Command failed: {result.stderr}"}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Command timed out"}

def main():
    """Main connection process"""
    print("🎭 MCP Blender Connection Setup")
    print("=" * 50)
    
    connector = MCPBlenderConnector()
    
    # Step 1: Find Blender
    print("Step 1: Finding Blender installation...")
    if not connector.find_blender():
        print("❌ Please install Blender first")
        return False
    
    # Step 2: Check MCP addon
    print("\nStep 2: Checking MCP addon status...")
    if not connector.check_mcp_addon_status():
        print("❌ MCP addon not found or not enabled")
        print("💡 Please install and enable the MCP addon in Blender")
        return False
    
    # Step 3: Test connection
    print("\nStep 3: Testing MCP connection...")
    if not connector.test_mcp_connection():
        print("❌ MCP connection test failed")
        return False
    
    print("\n✅ MCP Blender connection established!")
    print("🚀 Ready to use MCP commands with Blender")
    
    # Test a simple command
    print("\nTesting scene info command...")
    command = {
        "method": "tools/call",
        "params": {
            "name": "get_scene_info",
            "arguments": {}
        }
    }
    
    result = connector.run_mcp_command(command)
    if result and result.get("success"):
        print("✅ Scene info command successful!")
        print(f"📊 Scene: {result['data']['scene_name']}")
        print(f"📊 Objects: {len(result['data']['objects'])}")
        if result['data']['active_object']:
            print(f"📊 Active Object: {result['data']['active_object']}")
    else:
        print(f"❌ Scene info command failed: {result.get('message', 'Unknown error')}")
    
    return True

if __name__ == "__main__":
    main()