import socket
import threading
import sys
import os
import gzip



class HTTPServer:
    def __init__(self, host="localhost", port=4221):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = True

    def start(self):
        """Start the HTTP server."""
        self.server_socket = socket.create_server((self.host, self.port), reuse_port=False)
        print(f"Server started on {self.host}:{self.port}")
        print("Listening for connections...")

        while self.is_running:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Connection from {addr} has been established!")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"Active connections: {threading.activeCount() - 1}")
            except OSError:
                # Break the loop if the server socket is closed
                break

    def handle_client(self, conn, addr):
        """Handle a single client connection."""

        try:
            request = conn.recv(1024).decode('utf-8')
            print("Request received:", request)
            response = self.handle_api_request(request)
            while True:
                conn.sendall(response)
                try:
                    request = conn.recv(1024).decode('utf-8')
                    if not request.strip():
                        break
                    if self.extract_header_value(request, "Connection") == "close":
                        conn.sendall(self.http_response(200, "OK", "close", is_connection_close=True))
                        conn.close()
                        break
                    print("Request received:", request)
                    response = self.handle_api_request(request)
                except Exception as e:
                    print("Error handling client:", e)
                    break
        except Exception as e:
            print("Error handling client:", e)

    def handle_api_request(self, request):
        """Process the HTTP request and generate a response."""
        try:
            url_path = request.split(" ")[1]
            if url_path.startswith("/echo/"):
                return self.handle_echo(request, url_path)
            elif url_path.startswith("/user-agent"):
                return self.handle_user_agent(request)
            elif url_path.startswith("/files/"):
                return self.handle_file_operations(request, url_path)
            elif url_path == "/":
                return self.http_response(200, "OK", "")
            else:
                return self.http_response(404, "Not Found", "")
        except Exception as e:
            print("Error handling request:", e)
            return self.http_response(500, "Internal Server Error", "An error occurred.")

    def handle_echo(self, request, url_path):
        """Handle the /echo/ endpoint."""
        endpoint = url_path.split("/")[2]
        accept_encoding = self.extract_header_value(request, "Accept-Encoding")
        if accept_encoding and ('gzip' in accept_encoding or ' gzip' in accept_encoding):
            compressed_data = gzip.compress(endpoint.encode('utf-8'))
            return self.http_response(200, "OK", compressed_data, content_encoding="gzip")
        else:
            return self.http_response(200, "OK", endpoint)

    def handle_user_agent(self, request):
        """Handle the /user-agent endpoint."""
        user_agent = self.extract_header_value(request, "User-Agent")
        return self.http_response(200, "OK", user_agent)

    def handle_file_operations(self, request, url_path):
        """Handle file-related operations."""
        directory = sys.argv[2] if len(sys.argv) > 1 else None
        file_name = url_path.split("/")[2]
        http_method = request.split(" ")[0]

        if http_method == "POST":
            request_body = request.split("\r\n\r\n")[1]
            if directory and os.path.exists(directory):
                with open(os.path.join(directory, file_name), 'wb') as f:
                    f.write(request_body.encode())
                return self.http_response(201, "Created", "")
            else:
                return self.http_response(415, "Unsupported Media Type", "")
        elif http_method == "GET":
            if directory and os.path.isfile(os.path.join(directory, file_name)):
                with open(os.path.join(directory, file_name), 'rb') as f:
                    file_content = f.read()
                return self.http_response(200, "OK", file_content, content_type="application/octet-stream")
            else:
                return self.http_response(404, "Not Found", "")
        else:
            return self.http_response(405, "Method Not Allowed", "")

    def extract_header_value(self, request, header_name):
        """Extract the value of a specific header from the HTTP request."""
        lines = request.split("\r\n")
        for line in lines:
            if line.startswith(header_name):
                _, value = line.split(": ", 1)
                return value
        return None

    def http_response(self, status_code, status_message, body, is_connection_close=False, content_type="text/plain", content_encoding=None):
        """Generate an HTTP response."""
        headers = [
            f"HTTP/1.1 {status_code} {status_message}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body)}"
        ]
        if content_encoding:
            headers.append(f"Content-Encoding: {content_encoding}")
        if is_connection_close:
            headers.append("Connection: close")
        headers.append("\r\n")
        response = "\r\n".join(headers).encode('utf-8')
        if isinstance(body, str):
            response += body.encode('utf-8')
        else:
            response += body
        return response
    
    






def main():
    server = HTTPServer()


    # Start the server
    server.start()


if __name__ == "__main__":
    main()
