#!/usr/bin/env python3
"""
Simple Port 9876 Connection Test
"""

import socket
import json

def test_port_9876():
    """Test if port 9876 is accessible"""
    print("🔗 Testing port 9876 connection...")
    
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Try to connect
        result = sock.connect_ex(('localhost', 9876))
        
        if result == 0:
            print("✅ Port 9876 is open and accessible!")
            
            # Try to send a simple MCP request
            try:
                # Send MCP initialization
                init_request = {
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
                }
                
                request_data = json.dumps(init_request) + "\n"
                sock.send(request_data.encode())
                
                # Try to receive response
                sock.settimeout(2)
                response_data = sock.recv(1024).decode()
                
                if response_data:
                    print("📨 Received response from MCP server:")
                    print(response_data[:200] + "..." if len(response_data) > 200 else response_data)
                    
                    try:
                        response = json.loads(response_data.strip())
                        if "result" in response:
                            print("✅ MCP server responded successfully!")
                            return True
                        else:
                            print("❌ MCP server error response")
                            return False
                    except json.JSONDecodeError:
                        print("❌ Invalid JSON response from server")
                        return False
                else:
                    print("❌ No response from server")
                    return False
                    
            except Exception as e:
                print(f"❌ Error communicating with server: {e}")
                return False
            finally:
                sock.close()
        else:
            print("❌ Port 9876 is not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_alternative_ports():
    """Test common MCP ports"""
    print("\n🔍 Testing alternative MCP ports...")
    
    ports_to_test = [3000, 8000, 8080, 9000, 5000, 4000, 9876, 3001]
    
    for port in ports_to_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print(f"✅ Port {port} is open!")
            else:
                print(f"❌ Port {port} is closed")
                
        except Exception as e:
            print(f"❌ Port {port} error: {e}")

def main():
    """Main test function"""
    print("🎭 MCP Port Connection Test")
    print("=" * 40)
    
    # Test port 9876 specifically
    print("Testing port 9876 (your specified port)...")
    port_9876_success = test_port_9876()
    
    # Test other common ports
    test_alternative_ports()
    
    # Summary
    print("\n📋 CONNECTION SUMMARY:")
    print("=" * 25)
    
    if port_9876_success:
        print("✅ Port 9876: MCP server is running and accessible!")
        print("🚀 Ready to use MCP tools with Blender!")
    else:
        print("❌ Port 9876: Not accessible from this environment")
        print("💡 This could be because:")
        print("   • MCP server is running on a different machine")
        print("   • Firewall blocking the connection")
        print("   • Server is not running")
        print("   • This remote environment can't access your local server")
    
    return port_9876_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)