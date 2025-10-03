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