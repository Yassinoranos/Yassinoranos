#!/usr/bin/env python3
"""
Simple MCP Blender Server
This server provides MCP protocol communication for Blender operations
"""

import json
import sys
import subprocess
import os
from typing import Dict, Any, List

class MCPBlenderServer:
    def __init__(self):
        self.blender_path = None
        self.find_blender()
    
    def find_blender(self):
        """Try to find Blender installation"""
        possible_paths = [
            "/usr/bin/blender",
            "/usr/local/bin/blender",
            "/opt/blender/blender",
            "/snap/bin/blender",
            "blender"  # In PATH
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.blender_path = path
                    # Don't print to stdout as it interferes with MCP protocol
                    return
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        # Blender not found - this is expected in this environment
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        method = request.get("method", "")
        params = request.get("params", {})
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        }
                    },
                    "serverInfo": {
                        "name": "mcp-blender-server",
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "create_cube",
                            "description": "Create a cube in Blender",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "size": {
                                        "type": "number",
                                        "description": "Size of the cube",
                                        "default": 2.0
                                    }
                                }
                            }
                        },
                        {
                            "name": "get_blender_info",
                            "description": "Get information about Blender installation",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "get_scene_info",
                            "description": "Get information about the current Blender scene",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        },
                        {
                            "name": "reset_shape_keys",
                            "description": "Reset shape keys on selected mesh objects (useful for human faces)",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "object_name": {
                                        "type": "string",
                                        "description": "Name of the object to reset shape keys (optional, uses active object if not specified)",
                                        "default": ""
                                    },
                                    "reset_to_basis": {
                                        "type": "boolean",
                                        "description": "Reset all shape keys to basis (0) value",
                                        "default": True
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            
            if tool_name == "create_cube":
                return self.create_cube(arguments)
            elif tool_name == "get_blender_info":
                return self.get_blender_info()
            elif tool_name == "get_scene_info":
                return self.get_scene_info()
            elif tool_name == "reset_shape_keys":
                return self.reset_shape_keys(arguments)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }
    
    def create_cube(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a cube in Blender"""
        size = args.get("size", 2.0)
        
        if not self.blender_path:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: Blender not found. Please install Blender first."
                        }
                    ]
                }
            }
        
        # Create a simple Python script to run in Blender
        blender_script = f"""
import bpy

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a cube
bpy.ops.mesh.primitive_cube_add(size={size})

# Get the created cube
cube = bpy.context.active_object
cube.name = "MCP_Cube"

print(f"Cube created with size: {size}")
"""
        
        try:
            # Run the script in Blender
            result = subprocess.run([
                self.blender_path, 
                "--background", 
                "--python-expr", 
                blender_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Successfully created cube with size {size} in Blender!"
                            }
                        ]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error creating cube: {result.stderr}"
                            }
                        ]
                    }
                }
        except subprocess.TimeoutExpired:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: Blender operation timed out"
                        }
                    ]
                }
            }
    
    def get_blender_info(self) -> Dict[str, Any]:
        """Get information about Blender installation"""
        if not self.blender_path:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Blender not found. Please install Blender first."
                        }
                    ]
                }
            }
        
        try:
            result = subprocess.run([
                self.blender_path, "--version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Blender Info:\nPath: {self.blender_path}\nVersion:\n{result.stdout}"
                            }
                        ]
                    }
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error getting Blender info: {result.stderr}"
                            }
                        ]
                    }
                }
        except subprocess.TimeoutExpired:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: Blender version check timed out"
                        }
                    ]
                }
            }
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get information about the current Blender scene"""
        if not self.blender_path:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Blender not found. Please install Blender first."
                        }
                    ]
                }
            }
        
        # Create a script to get scene information
        blender_script = """
import bpy
import json

scene_info = {
    "scene_name": bpy.context.scene.name,
    "objects": [],
    "materials": [],
    "lights": [],
    "cameras": [],
    "meshes": []
}

# Get all objects in the scene
for obj in bpy.context.scene.objects:
    obj_info = {
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale),
        "visible": obj.visible_get()
    }
    
    if obj.type == 'MESH':
        obj_info["vertices"] = len(obj.data.vertices)
        obj_info["faces"] = len(obj.data.polygons)
        obj_info["edges"] = len(obj.data.edges)
    
    scene_info["objects"].append(obj_info)

# Get materials
for mat in bpy.data.materials:
    scene_info["materials"].append({
        "name": mat.name,
        "use_nodes": mat.use_nodes
    })

# Get lights
for light in bpy.data.lights:
    scene_info["lights"].append({
        "name": light.name,
        "type": light.type,
        "energy": light.energy
    })

# Get cameras
for camera in bpy.data.cameras:
    scene_info["cameras"].append({
        "name": camera.name,
        "type": camera.type,
        "lens": camera.lens
    })

# Get meshes
for mesh in bpy.data.meshes:
    scene_info["meshes"].append({
        "name": mesh.name,
        "vertices": len(mesh.vertices),
        "faces": len(mesh.polygons),
        "edges": len(mesh.edges)
    })

print("SCENE_INFO_START")
print(json.dumps(scene_info, indent=2))
print("SCENE_INFO_END")
"""
        
        try:
            # Run the script in Blender
            result = subprocess.run([
                self.blender_path, 
                "--background", 
                "--python-expr", 
                blender_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse the output to extract scene info
                output = result.stdout
                if "SCENE_INFO_START" in output and "SCENE_INFO_END" in output:
                    start_idx = output.find("SCENE_INFO_START") + len("SCENE_INFO_START")
                    end_idx = output.find("SCENE_INFO_END")
                    scene_json = output[start_idx:end_idx].strip()
                    
                    try:
                        scene_data = json.loads(scene_json)
                        return {
                            "jsonrpc": "2.0",
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Current Blender Scene Information:\n\nScene: {scene_data['scene_name']}\n\nObjects ({len(scene_data['objects'])}):\n" + 
                                               "\n".join([f"- {obj['name']} ({obj['type']}) at {obj['location']}" for obj in scene_data['objects']]) +
                                               f"\n\nMaterials ({len(scene_data['materials'])}):\n" +
                                               "\n".join([f"- {mat['name']}" for mat in scene_data['materials']]) +
                                               f"\n\nLights ({len(scene_data['lights'])}):\n" +
                                               "\n".join([f"- {light['name']} ({light['type']})" for light in scene_data['lights']]) +
                                               f"\n\nCameras ({len(scene_data['cameras'])}):\n" +
                                               "\n".join([f"- {cam['name']} ({cam['type']})" for cam in scene_data['cameras']])
                                    }
                                ]
                            }
                        }
                    except json.JSONDecodeError:
                        return {
                            "jsonrpc": "2.0",
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Error parsing scene data: {scene_json}"
                                    }
                                ]
                            }
                        }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Scene info not found in output. Raw output:\n{output}"
                                }
                            ]
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error getting scene info: {result.stderr}"
                            }
                        ]
                    }
                }
        except subprocess.TimeoutExpired:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: Blender scene check timed out"
                        }
                    ]
                }
            }
    
    def reset_shape_keys(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Reset shape keys on mesh objects (useful for human faces)"""
        if not self.blender_path:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Blender not found. Please install Blender first."
                        }
                    ]
                }
            }
        
        object_name = args.get("object_name", "")
        reset_to_basis = args.get("reset_to_basis", True)
        
        # Create a script to reset shape keys
        blender_script = f"""
import bpy
import json

# Function to reset shape keys
def reset_shape_keys(obj_name="", reset_to_basis=True):
    result_info = {{
        "success": False,
        "object_name": "",
        "shape_keys_reset": 0,
        "message": ""
    }}
    
    try:
        # Select the object
        if obj_name:
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                bpy.context.view_layer.objects.active = obj
                obj.select_set(True)
            else:
                result_info["message"] = f"Object '{{obj_name}}' not found"
                return result_info
        else:
            # Use active object
            obj = bpy.context.active_object
            if not obj:
                result_info["message"] = "No active object selected"
                return result_info
        
        if obj.type != 'MESH':
            result_info["message"] = f"Object '{{obj.name}}' is not a mesh"
            return result_info
        
        if not obj.data.shape_keys:
            result_info["message"] = f"Object '{{obj.name}}' has no shape keys"
            return result_info
        
        result_info["object_name"] = obj.name
        
        # Reset all shape keys
        shape_keys = obj.data.shape_keys
        key_blocks = shape_keys.key_blocks
        
        reset_count = 0
        for key_block in key_blocks:
            if key_block.name != "Basis":  # Don't reset the basis shape
                if reset_to_basis:
                    key_block.value = 0.0  # Reset to basis
                else:
                    # Reset to neutral position (interpolate between basis and current)
                    key_block.value = 0.0
                reset_count += 1
        
        result_info["success"] = True
        result_info["shape_keys_reset"] = reset_count
        result_info["message"] = f"Successfully reset {{reset_count}} shape keys on '{{obj.name}}'"
        
        # Update the mesh
        obj.data.update()
        
    except Exception as e:
        result_info["message"] = f"Error resetting shape keys: {{str(e)}}"
    
    return result_info

# Execute the reset
result = reset_shape_keys("{object_name}", {str(reset_to_basis).lower()})

print("SHAPE_KEY_RESET_START")
print(json.dumps(result, indent=2))
print("SHAPE_KEY_RESET_END")
"""
        
        try:
            # Run the script in Blender
            result = subprocess.run([
                self.blender_path, 
                "--background", 
                "--python-expr", 
                blender_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse the output to extract result
                output = result.stdout
                if "SHAPE_KEY_RESET_START" in output and "SHAPE_KEY_RESET_END" in output:
                    start_idx = output.find("SHAPE_KEY_RESET_START") + len("SHAPE_KEY_RESET_START")
                    end_idx = output.find("SHAPE_KEY_RESET_END")
                    result_json = output[start_idx:end_idx].strip()
                    
                    try:
                        reset_data = json.loads(result_json)
                        if reset_data["success"]:
                            return {
                                "jsonrpc": "2.0",
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"✅ Shape Keys Reset Successful!\n\n"
                                                   f"Object: {reset_data['object_name']}\n"
                                                   f"Shape Keys Reset: {reset_data['shape_keys_reset']}\n"
                                                   f"Message: {reset_data['message']}\n\n"
                                                   f"🎭 Your human face should now be back to its neutral expression!"
                                        }
                                    ]
                                }
                            }
                        else:
                            return {
                                "jsonrpc": "2.0",
                                "result": {
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"❌ Shape Key Reset Failed\n\nMessage: {reset_data['message']}"
                                        }
                                    ]
                                }
                            }
                    except json.JSONDecodeError:
                        return {
                            "jsonrpc": "2.0",
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Error parsing reset data: {result_json}"
                                    }
                                ]
                            }
                        }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Reset result not found in output. Raw output:\n{output}"
                                }
                            ]
                        }
                    }
            else:
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Error resetting shape keys: {result.stderr}"
                            }
                        ]
                    }
                }
        except subprocess.TimeoutExpired:
            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": "Error: Blender shape key reset timed out"
                        }
                    ]
                }
            }

def main():
    """Main function to run the MCP server"""
    server = MCPBlenderServer()
    
    # Don't print debug messages to stdout as it interferes with MCP protocol
    # Use stderr for debug messages instead
    sys.stderr.write("MCP Blender Server starting...\n")
    sys.stderr.write("Listening for MCP requests on stdin/stdout\n")
    
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            
            try:
                request = json.loads(line.strip())
                response = server.handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }))
                sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stderr.write("Server shutting down...\n")

if __name__ == "__main__":
    main()