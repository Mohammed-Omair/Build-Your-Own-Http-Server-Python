import socket  # noqa: F401
import threading
import sys
import os
import gzip

def handle_client(client_socket):
    # Receive the client's request
    request = client_socket.recv(1024)
    args = sys.argv
    response(client_socket, request, args)
    # Close the client connection
    client_socket.close()

def file_details(file_path):
    file_size = os.stat(file_path).st_size
    with open(file_path, 'r') as file:
        file_data = file.read()
    return file_size, file_data

def response(client_socket, request, args):
    decoded_request = request.decode("utf-8").split()
    file_path = args[-1] + (decoded_request[1].split("/")[-1])
    if decoded_request[0] == "GET":
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
        elif "files" in decoded_request[1] and os.path.exists(file_path):
            file_size, file_data = file_details(file_path)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {file_size}\r\n\r\n{file_data}"
            response = response.encode("utf-8")
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    elif decoded_request[0] == "POST":
        if "files" in decoded_request[1]:
            position = request.find(b"\r\n\r\n")
            body = request[position + 4:]
            data = body.decode("utf-8")
            with open(file_path, "w") as f:
                f.write(data)
            response = b"HTTP/1.1 201 Created\r\n\r\n"
    if b"Accept-Encoding" in request and b"gzip" in request:
        response = response.decode("utf-8")
        header_part, body_part = response.split("\r\n\r\n", 1)
        compressed_data = gzip.compress(body_part.encode("utf-8"))  # Compressing as gzip
        # Add the new header
        updated_file_size = len(compressed_data)  # or any new size you need to set
        header_lines = header_part.split("\r\n")
        header_part = "\r\n".join(
            line if not line.startswith("Content-Length:") else f"Content-Length: {updated_file_size}"
            for line in header_lines
        )
        header_part += "\r\nContent-Encoding: gzip"
        # Reassemble the response
        response = f"{header_part}\r\n\r\n"
        response = response.encode("utf-8")
        response += compressed_data
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
