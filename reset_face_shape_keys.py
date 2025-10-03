#!/usr/bin/env python3
"""
Reset Shape Keys on Human Face via MCP
"""

import json
import subprocess
import sys

def reset_face_shape_keys(object_name=""):
    """Reset shape keys on human face object"""
    
    # Request to reset shape keys
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "reset_shape_keys",
            "arguments": {
                "object_name": object_name,
                "reset_to_basis": True
            }
        }
    }
    
    print("🎭 Resetting Shape Keys on Human Face...")
    print("=" * 50)
    
    if object_name:
        print(f"Target Object: {object_name}")
    else:
        print("Target Object: Active Object (will be detected)")
    print()
    
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
                    result_text = response["result"]["content"][0]["text"]
                    print(result_text)
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
        print(f"Error during shape key reset: {e}")

if __name__ == "__main__":
    # You can specify the object name here, or leave empty to use active object
    target_object = ""  # Change this to your face object name if needed
    reset_face_shape_keys(target_object)