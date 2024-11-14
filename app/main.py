import socket  # Socket library for networking
import threading  # Library for handling multiple clients concurrently
import sys  # Library for system-level operations and arguments
import os  # Library for file handling
import gzip  # Library for gzip compression

def handle_client(client_socket):
    """
    Handles communication with a single client. Receives the request,
    processes it, and sends the response.
    """
    # Receive the client's initial request (up to 1024 bytes)
    request = client_socket.recv(1024)
    
    # Retrieve command-line arguments
    args = sys.argv

    # Process the request and prepare a response
    response(client_socket, request, args)
    
    # Close the client connection after responding
    client_socket.close()

def file_details(file_path):
    """
    Retrieves the file size and contents for a given file path.
    """
    # Get the size of the file in bytes
    file_size = os.stat(file_path).st_size
    
    # Read the contents of the file
    with open(file_path, 'r') as file:
        file_data = file.read()
    
    return file_size, file_data

def response(client_socket, request, args):
    """
    Processes the HTTP request and generates an appropriate HTTP response.
    Supports GET, POST, and gzip-encoded responses.
    """
    # Decode and parse the request into parts
    decoded_request = request.decode("utf-8").split()
    
    # Construct the file path from the arguments and request URI
    file_path = args[-1] + (decoded_request[1].split("/")[-1])

    # Handle GET requests
    if decoded_request[0] == "GET":
        # Root request ("/")
        if decoded_request[1] == '/':
            response = b"HTTP/1.1 200 OK\r\n\r\n"
        
        # Echo endpoint for testing
        elif "echo" in decoded_request[1]:
            echo_endpoint = decoded_request[1].split("/")[2]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_endpoint)}\r\n\r\n{echo_endpoint}"
            response = response.encode("utf-8")
        
        # User-agent endpoint (for demonstration)
        elif "user-agent" in decoded_request[1]:
            user_agent_endpoint = decoded_request[-1]
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent_endpoint)}\r\n\r\n{user_agent_endpoint}"
            response = response.encode("utf-8")
        
        # File retrieval for "files" endpoint if the file exists
        elif "files" in decoded_request[1] and os.path.exists(file_path):
            file_size, file_data = file_details(file_path)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {file_size}\r\n\r\n{file_data}"
            response = response.encode("utf-8")
        
        # Respond with 404 if the file or endpoint is not found
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n"
    
    # Handle POST requests
    elif decoded_request[0] == "POST":
        # Save the file sent in the POST body if the request is to "files"
        if "files" in decoded_request[1]:
            position = request.find(b"\r\n\r\n")
            body = request[position + 4:]  # Extract the body after headers
            data = body.decode("utf-8")
            # Write data to the specified file
            with open(file_path, "w") as f:
                f.write(data)
            response = b"HTTP/1.1 201 Created\r\n\r\n"

    # Handle gzip compression if "Accept-Encoding: gzip" is in request headers
    if b"Accept-Encoding" in request and b"gzip" in request:
        # Decode response to work with headers and body separately
        response = response.decode("utf-8")
        
        # Split headers and body
        header_part, body_part = response.split("\r\n\r\n", 1)
        
        # Compress the body content with gzip
        compressed_data = gzip.compress(body_part.encode("utf-8"))
        
        # Update Content-Length to reflect the compressed size
        updated_file_size = len(compressed_data)
        
        # Update headers by replacing Content-Length with the new size
        header_lines = header_part.split("\r\n")
        header_part = "\r\n".join(
            line if not line.startswith("Content-Length:") else f"Content-Length: {updated_file_size}"
            for line in header_lines
        )
        
        # Add the Content-Encoding header to specify gzip encoding
        header_part += "\r\nContent-Encoding: gzip"
        
        # Reassemble headers and compressed body into the final response
        response = f"{header_part}\r\n\r\n".encode("utf-8") + compressed_data
    
    # Send the final response to the client
    client_socket.send(response)

def main():
    """
    Sets up the server to listen for incoming connections, and spawns a new
    thread to handle each client connection.
    """
    # Create the server socket and bind to localhost on port 4221
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221...")

    while True:
        # Accept a new client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Create a new thread for each client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()  # Start the thread to handle the client

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
