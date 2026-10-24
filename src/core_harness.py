# src/core_harness.py
import socket
import json

IP_ADDRESS = '127.0.0.1'
PORT = 1234

def execute_raw_post(api_path, json_payload):
    """Sends a raw HTTP POST frame over low-level sockets to bypass proxy blocks."""
    http_request = (
        f"POST {api_path} HTTP/1.1\r\n"
        f"Host: {IP_ADDRESS}:{PORT}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(json_payload)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{json_payload}"
    )
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(None) # Wait patiently for local hardware inference cycles
    
    try:
        s.connect((IP_ADDRESS, PORT))
        s.sendall(http_request.encode('utf-8'))
        
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        return response.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"SOCKET_ERROR: {e}"
    finally:
        s.close()
