import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn,addr = server_socket.accept()
    print(f"Connection from {addr} has been established!");
    print("conn",conn)
    request = conn.recv(1024).decode('utf-8')
    print("request",request)
    print("request split",request.split("\r\n"))
    headerInfoValue = request.split("\r\n")[2].split(": ")
    url_path = request.split(" ")[1]
    # if url_path.startswith("/echo/"):
    #     endpoint = url_path.split("/")[2]
    #     print("endpoint",endpoint)
    #     _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(endpoint)}\r\n\r\n{endpoint}"
    #     response =  _response.encode('utf-8')
    # elif url_path == "/":
    #     response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    # else:
    #     response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    if url_path.startswith("/user-agent"):
        _response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length:{len(headerInfoValue)}\r\n\r\n{headerInfoValue}"
        response =  _response.encode('utf-8')
    elif url_path == "/":
        response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 0\r\n\r\n"
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
            
    conn.sendall(response)
    conn.close()
    


if __name__ == "__main__":
    main()
