#!/usr/bin/env python3
"""
Check Blender Scene via MCP
"""

import json
import subprocess
import sys

def check_blender_scene():
    """Check what's in the current Blender scene"""
    
    # Request to get scene info
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_scene_info",
            "arguments": {}
        }
    }
    
    print("Checking Blender scene...")
    print("=" * 50)
    
    try:
        # Start the MCP server
        process = subprocess.Popen(
            [sys.executable, "/workspace/mcp_blender_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send request
        process.stdin.write(json.dumps(request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            try:
                response = json.loads(response_line.strip())
                if "result" in response and "content" in response["result"]:
                    scene_info = response["result"]["content"][0]["text"]
                    print(scene_info)
                else:
                    print(f"Unexpected response format: {response}")
            except json.JSONDecodeError:
                print(f"Invalid JSON response: {response_line}")
        else:
            print("No response received")
        
        # Close the process
        process.stdin.close()
        process.wait(timeout=10)
        
    except subprocess.TimeoutExpired:
        print("Process timed out")
        process.kill()
    except Exception as e:
        print(f"Error during scene check: {e}")

if __name__ == "__main__":
    check_blender_scene()