import socket  # noqa: F401
import threading

def handle_client(client_socket):
    # Receive the client's request
    request = client_socket.recv(1024)
    # Process and respond to the client
    response(client_socket, request)
    # Close the client connection
    client_socket.close()

def response(client_socket, request):
    decoded_request = request.decode("utf-8").split()
    if decoded_request[1] == '/':
        response = b"HTTP/1.1 200 OK\r\n\r\n"
    elif "echo" in decoded_request[1]:
        echo_endpoint = decoded_request[1].split("/")[2]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_endpoint)}\r\n\r\n{echo_endpoint}"
        response = response.encode("utf-8")
    elif "user-agent" in decoded_request[1]:
        user_agent_endpoint = decoded_request[-1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_endpoint)}\r\n\r\n{user_agent_endpoint}"
        response = response.encode("utf-8")
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    client_socket.send(response)
    


def main():
    # Create the server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
