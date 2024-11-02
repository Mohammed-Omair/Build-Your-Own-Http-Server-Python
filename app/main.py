import socket  # noqa: F401


def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client
    request = client_socket.recv(1024)
    response = b"HTTP/1.1 200 OK\r\n"
    client_socket.send(response)

if __name__ == "__main__":
    main()
