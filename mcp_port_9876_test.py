#!/usr/bin/env python3
"""
MCP Connection Test for Port 9876
"""

import json
import socket
import time

def test_mcp_port_9876():
    """Test MCP connection on port 9876"""
    print("🔗 Testing MCP connection on port 9876...")
    
    try:
        # Connect to MCP server on port 9876
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        print("✅ Connected to MCP server on port 9876!")
        
        # Send MCP initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "blender-mcp-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send request
        request_data = json.dumps(init_request) + "\n"
        sock.send(request_data.encode())
        
        # Receive response
        response_data = sock.recv(4096).decode()
        print("📨 Received response:")
        print(response_data)
        
        # Parse response
        try:
            response = json.loads(response_data.strip())
            if "result" in response:
                print("✅ MCP initialization successful!")
                print(f"📊 Server: {response['result'].get('serverInfo', {}).get('name', 'Unknown')}")
                print(f"📊 Version: {response['result'].get('serverInfo', {}).get('version', 'Unknown')}")
                return True
            else:
                print("❌ MCP initialization failed")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid JSON response")
            return False
            
    except ConnectionRefusedError:
        print("❌ Connection refused - no server on port 9876")
        return False
    except socket.timeout:
        print("❌ Connection timeout")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def test_blender_tools_port_9876():
    """Test Blender-specific tools on port 9876"""
    print("\n🛠️ Testing Blender tools on port 9876...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        # Test tools/list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        request_data = json.dumps(tools_request) + "\n"
        sock.send(request_data.encode())
        
        response_data = sock.recv(4096).decode()
        print("📋 Available tools:")
        
        try:
            response = json.loads(response_data.strip())
            if "result" in response and "tools" in response["result"]:
                tools = response["result"]["tools"]
                print(f"✅ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  • {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
                return tools
            else:
                print("❌ No tools found in response")
                return []
        except json.JSONDecodeError:
            print("❌ Invalid tools response")
            return []
            
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        return []
    finally:
        try:
            sock.close()
        except:
            pass

def test_blender_scene_info():
    """Test getting Blender scene information"""
    print("\n🎬 Testing Blender scene info...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        # Test scene info
        scene_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_scene_info",
                "arguments": {}
            }
        }
        
        request_data = json.dumps(scene_request) + "\n"
        sock.send(request_data.encode())
        
        response_data = sock.recv(4096).decode()
        print("📊 Scene information:")
        
        try:
            response = json.loads(response_data.strip())
            if "result" in response and "content" in response["result"]:
                content = response["result"]["content"][0]["text"]
                print(content)
                return True
            else:
                print("❌ No scene info in response")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid scene response")
            return False
            
    except Exception as e:
        print(f"❌ Error getting scene info: {e}")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def test_face_shape_key_reset():
    """Test face shape key reset"""
    print("\n🎭 Testing face shape key reset...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        # Test shape key reset
        reset_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "reset_shape_keys",
                "arguments": {
                    "object_name": "",
                    "reset_to_basis": True
                }
            }
        }
        
        request_data = json.dumps(reset_request) + "\n"
        sock.send(request_data.encode())
        
        response_data = sock.recv(4096).decode()
        print("🎭 Shape key reset result:")
        
        try:
            response = json.loads(response_data.strip())
            if "result" in response and "content" in response["result"]:
                content = response["result"]["content"][0]["text"]
                print(content)
                return True
            else:
                print("❌ No reset result in response")
                return False
        except json.JSONDecodeError:
            print("❌ Invalid reset response")
            return False
            
    except Exception as e:
        print(f"❌ Error resetting shape keys: {e}")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def main():
    """Main test function"""
    print("🎭 MCP Blender Connection Test - Port 9876")
    print("=" * 60)
    
    # Test 1: Basic connection
    print("Test 1: MCP Server Connection")
    connected = test_mcp_port_9876()
    
    if not connected:
        print("\n❌ Cannot proceed - MCP server not accessible")
        return False
    
    # Test 2: Available tools
    print("\nTest 2: Available Tools")
    tools = test_blender_tools_port_9876()
    
    # Test 3: Scene info
    print("\nTest 3: Blender Scene Info")
    scene_success = test_blender_scene_info()
    
    # Test 4: Shape key reset
    print("\nTest 4: Face Shape Key Reset")
    reset_success = test_face_shape_key_reset()
    
    # Summary
    print("\n📋 CONNECTION SUMMARY:")
    print("=" * 30)
    print(f"MCP Server (9876): {'✅ Connected' if connected else '❌ Failed'}")
    print(f"Available Tools: {'✅ Found' if tools else '❌ None'}")
    print(f"Scene Info: {'✅ Working' if scene_success else '❌ Failed'}")
    print(f"Shape Key Reset: {'✅ Working' if reset_success else '❌ Failed'}")
    
    if connected and tools:
        print("\n🎉 SUCCESS! MCP Blender connection is working!")
        print("🚀 You can now control Blender via MCP on port 9876!")
        return True
    else:
        print("\n⚠️ MCP connection partially working")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)