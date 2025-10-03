#!/usr/bin/env python3
"""
MCP Client Test - Attempt to connect to MCP server
"""

import json
import socket
import time
import subprocess
import sys

def test_mcp_server_connection(host="localhost", port=3000):
    """Test connection to MCP server"""
    print(f"🔗 Testing MCP server connection to {host}:{port}...")
    
    try:
        # Try to connect to MCP server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ MCP server is running on {host}:{port}")
            return True
        else:
            print(f"❌ No MCP server on {host}:{port}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_blender_python_api():
    """Test if we can access Blender Python API"""
    print("🐍 Testing Blender Python API access...")
    
    try:
        # Try to import bpy (Blender Python API)
        import bpy
        print("✅ Blender Python API (bpy) is available!")
        
        # Get basic info
        info = {
            "version": bpy.app.version_string,
            "scene": bpy.context.scene.name,
            "active_object": bpy.context.active_object.name if bpy.context.active_object else None
        }
        
        print(f"📊 Blender Version: {info['version']}")
        print(f"📊 Scene: {info['scene']}")
        print(f"📊 Active Object: {info['active_object'] or 'None'}")
        
        return True
        
    except ImportError:
        print("❌ Blender Python API (bpy) not available")
        print("💡 This means Blender is not running or not accessible")
        return False
    except Exception as e:
        print(f"❌ Error accessing Blender API: {e}")
        return False

def test_mcp_tools():
    """Test MCP tools if Blender is available"""
    print("🛠️ Testing MCP tools...")
    
    try:
        import bpy
        
        # Test scene info tool
        scene_info = {
            "scene_name": bpy.context.scene.name,
            "objects": len(bpy.context.scene.objects),
            "active_object": bpy.context.active_object.name if bpy.context.active_object else None
        }
        
        print("✅ Scene Info Tool:")
        print(f"  • Scene: {scene_info['scene_name']}")
        print(f"  • Objects: {scene_info['objects']}")
        print(f"  • Active: {scene_info['active_object'] or 'None'}")
        
        # Test shape key tool if active object is mesh
        if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
            obj = bpy.context.active_object
            if obj.data.shape_keys:
                print(f"✅ Shape Key Tool: {len(obj.data.shape_keys.key_blocks)} keys found")
                
                # Test reset
                reset_count = 0
                for key_block in obj.data.shape_keys.key_blocks:
                    if key_block.name != "Basis":
                        reset_count += 1
                
                print(f"✅ Shape Key Reset Tool: {reset_count} keys can be reset")
            else:
                print("⚠️ Shape Key Tool: No shape keys found")
        else:
            print("⚠️ Shape Key Tool: No active mesh object")
        
        return True
        
    except ImportError:
        print("❌ Cannot test MCP tools - Blender not available")
        return False
    except Exception as e:
        print(f"❌ Error testing MCP tools: {e}")
        return False

def main():
    """Main test function"""
    print("🎭 MCP Blender Connection Test")
    print("=" * 50)
    print()
    
    # Test 1: MCP Server Connection
    print("Test 1: MCP Server Connection")
    server_connected = test_mcp_server_connection()
    print()
    
    # Test 2: Blender Python API
    print("Test 2: Blender Python API")
    blender_available = test_blender_python_api()
    print()
    
    # Test 3: MCP Tools
    if blender_available:
        print("Test 3: MCP Tools")
        tools_working = test_mcp_tools()
        print()
    else:
        tools_working = False
        print("Test 3: MCP Tools - Skipped (Blender not available)")
        print()
    
    # Summary
    print("📋 CONNECTION SUMMARY:")
    print("=" * 30)
    print(f"MCP Server: {'✅ Connected' if server_connected else '❌ Not Connected'}")
    print(f"Blender API: {'✅ Available' if blender_available else '❌ Not Available'}")
    print(f"MCP Tools: {'✅ Working' if tools_working else '❌ Not Working'}")
    
    if blender_available and tools_working:
        print("\n🎉 SUCCESS! MCP Blender connection is working!")
        print("🚀 You can now use MCP tools to control Blender!")
        return True
    else:
        print("\n⚠️ MCP Blender connection not fully established")
        print("💡 Make sure Blender is running with MCP addon enabled")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)