import socket  # noqa: F401
import threading
import sys
import os


def client_thread(conn, addr):
    print(f"Connection from {addr} has been established!")
    request = conn.recv(1024).decode('utf-8')
    print("request", request)
    response = handle_api_request(request)
    conn.sendall(response)


def extract_header_value(request, header_name):
    # Split the request into lines
    lines = request.split("\r\n")
    
    # Iterate through the lines to find the header
    for line in lines:
        if line.startswith(header_name):
            # Split the line into key and value
            _, value = line.split(": ", 1)
            return value.strip()
    
    return None


def handle_api_request(request):
    print("request", request)
    print("request split", request.split("\r\n"))
    print("arguments", sys.argv)
    url_path = request.split(" ")[1]
    if url_path.startswith("/echo/"):
        endpoint = url_path.split("/")[2]
        accept_encoding = extract_header_value(request, "Accept-Encoding")
        print("accept_encoding", accept_encoding)
        print("endpoint", endpoint)
        _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain{'\r\nContent-Encoding: ' + accept_encoding if accept_encoding == 'gzip' else ''}\r\nContent-Length:{len(endpoint)}\r\n\r\n{endpoint}"
        response = _response.encode('utf-8')
    elif url_path.startswith("/user-agent"):
        headerInfoValue = extract_header_value(request, "User-Agent")
        print("headerInfoValue", headerInfoValue)
        _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(headerInfoValue)}\r\n\r\n{headerInfoValue}"
        response = _response.encode('utf-8')
    elif url_path.startswith("/files/"):
        directory = None
        if len(sys.argv) > 1:
            directory = sys.argv[2]
        file_name = url_path.split("/")[2]
        print("file_name", file_name)
        
        httpMethod = request.split(" ")[0]
        print("httpMethod", httpMethod)
        
        if httpMethod == "POST":
            requestBody = request.split("\r\n\r\n")[1]
            print("requestBody", requestBody)
            if os.path.exists(directory):
                with open(os.path.join(directory, file_name), 'wb') as f:
                    f.write(requestBody.encode())
                    response = b"HTTP/1.1 201 Created\r\n\r\n"
            else:
                response = b"HTTP/1.1 415 Unsupported Media Type\r\n\r\n"
            
        elif httpMethod == "GET":
            if os.path.isfile(os.path.join(directory, file_name)):
                with open(os.path.join(directory, file_name), 'rb') as f:
                    file_content = f.read()
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: " + str(len(file_content)).encode() + b"\r\n\r\n" + file_content
        
            else:
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
    elif url_path == "/":
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
        
    return response


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    with socket.create_server(("localhost", 4221), reuse_port=False) as server_socket:
        print("Server started on port 4221")
        print("Listening for connections...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr} has been established!")
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()
            print(f"Active connections: {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()
