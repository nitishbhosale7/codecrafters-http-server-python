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
    


if __name__ == "__main__":
    main()
