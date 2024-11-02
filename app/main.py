import socket  # noqa: F401

def response(client_socket, request):
    decoded_request = request.decode("utf-8").split()
    if decoded_request[1] == '/abcdefg':
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif decoded_request[1] == '/':
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response)
    


def main():
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept() # wait for client
    request = client_socket.recv(1024)
    response(client_socket, request)


if __name__ == "__main__":
    main()
