#!/usr/bin/env python3
"""
Test MCP Connection with Blender
This script tests the MCP communication protocol
"""

import json
import subprocess
import sys
import time

def test_mcp_connection():
    """Test MCP connection with our server"""
    
    # Test requests
    test_requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        },
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        },
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_blender_info",
                "arguments": {}
            }
        }
    ]
    
    print("Testing MCP Connection...")
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
        
        # Send test requests
        for i, request in enumerate(test_requests):
            print(f"\nTest {i+1}: {request['method']}")
            print(f"Request: {json.dumps(request, indent=2)}")
            
            # Send request
            process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            
            # Read response
            response_line = process.stdout.readline()
            if response_line:
                try:
                    response = json.loads(response_line.strip())
                    print(f"Response: {json.dumps(response, indent=2)}")
                except json.JSONDecodeError:
                    print(f"Invalid JSON response: {response_line}")
            else:
                print("No response received")
            
            time.sleep(0.5)  # Small delay between requests
        
        # Close the process
        process.stdin.close()
        process.wait(timeout=5)
        
        print("\n" + "=" * 50)
        print("MCP Connection Test Complete!")
        
    except subprocess.TimeoutExpired:
        print("Process timed out")
        process.kill()
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_mcp_connection()