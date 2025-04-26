import socket  # noqa: F401
import threading



def client_thread(conn, addr):
    print(f"Connection from {addr} has been established!")
    request = conn.recv(1024).decode('utf-8')
    print("request",request)
    response = handle_api_request(request)
    conn.sendall(response)
    

    


def handle_api_request(request):
    print("request",request)
    print("request split",request.split("\r\n"))
    url_path = request.split(" ")[1]
    if url_path.startswith("/echo/"):
        endpoint = url_path.split("/")[2]
        print("endpoint",endpoint)
        _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(endpoint)}\r\n\r\n{endpoint}"
        response =  _response.encode('utf-8')
    elif url_path.startswith("/user-agent"):
        headerInfoValue = request.split("\r\n")[2].split(": ")[1]
        print("headerInfoValue",headerInfoValue)
        _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(headerInfoValue)}\r\n\r\n{headerInfoValue}"
        response =  _response.encode('utf-8')
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
            thread = threading.Thread(target=client_thread, args=(conn, addr))
            thread.start()
            print(f"Active connections: {threading.activeCount() - 1}")
            
    
    


if __name__ == "__main__":
    main()
