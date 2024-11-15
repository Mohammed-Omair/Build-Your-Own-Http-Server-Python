[![progress-banner](https://backend.codecrafters.io/progress/http-server/ad75c9d3-0640-4b2c-af79-6364ae55e602)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)



# Build Your Own HTTP server

A lightweight HTTP server built in Python that handles multiple clients using multithreading. This server supports basic HTTP GET and POST requests, dynamic file serving, and gzip compression for optimized data transfer. Ideal for testing simple HTTP interactions, exploring server fundamentals, and learning about HTTP header and body handling.

## Features

- **Multithreaded Connection Handling**: Efficiently manages multiple client connections concurrently, thanks to Python’s `threading` module.
- **GET and POST Request Support**:
  - **GET**: Handles requests for basic endpoints, including `/echo`, `/user-agent`, and `/files`.
  - **POST**: Supports file upload through the `/files` endpoint.
- **Dynamic File Serving**: Retrieves files from the server's directory and serves them with accurate `Content-Length` and `Content-Type` headers.
- **Gzip Compression**: Compresses the response body with gzip when the client specifies `Accept-Encoding: gzip`, providing faster data transfer for clients that support gzip encoding.
- **Custom Headers and Echo Endpoints**: Processes custom headers like `User-Agent` and an `/echo` endpoint to return specific data back to the client.

## Requirements

- Python 3.6+
- `curl` (for testing HTTP requests from the command line, optional)

## Code Overview
The main components of the server are:

1. `handle_client`: Manages each client connection by receiving the request, processing it, and sending the response. It can also handle concurrent requests.
2. `response`: Generates the HTTP response based on the request type and endpoint. Supports gzip compression if requested by the client.
3. `file_details`: Reads a specified file, returning its size and contents.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Mohammed-Omair/Build-Your-Own-Http-Server-Python.git
cd Build-Your-Own-Http-Server-Python/app/
```

### Run the Server
To start the server.
```bash
python3 main.py
```
This starts the server on `localhost` at port `4221`.

For operations that include files, `--directory` flag should be used and an appropraite directory should be provided.
```bash
python3 main.py --directory /tmp/
```

**Note**: It is recommended to run this on a linux operating system. However, if you are running it on windows, edit line number `124` and change "True" to "False"
```python
 server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
 ```

## Usage Instructions
With the server running, you can use `curl` to interact with it. 
Here are some sample requests:

### GET Requests

#### 1. Root Endpoint
```bash
curl -v http://localhost:4221/
```
Response: Basic 200 OK response.

#### 2. Echo Endpoint
```bash
curl -v http://localhost:4221/echo/hello
```
Response: Returns "hello" as plain text.

#### 3. User-Agent Header
```bash
curl -v -H "User-Agent: CustomAgent" http://localhost:4221/user-agent
```
Response: Echoes back the User-Agent header value.

#### 4. File Download
Place a file in the server directory (e.g., `sample.txt`) and request it:
```bash
curl -v http://localhost:4221/files/sample.txt
```
**Note**: This will not work if the `--directory` argument is not provided while starting the server.
### POST Requests

#### 1. File Upload
Upload a file (e.g., `testfile`) to the server:
```bash
curl -v --data "Hello" -H "Content-Type: application/octet-stream" http://localhost:4221/files/testfile
```
This saves `testfile.txt` to the server directory as uploaded.txt

**Note**: This will not work if the `--directory` argument is not provided while starting the server.
### Gzip Compression
To request gzip-encoded responses:
```bash
curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/compress_me
```
If gzip is supported, the server compresses the response body and sends it with the `Content-Encoding: gzip` header.

## Example Responses
- GET `/echo/test`:
```plaintext
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 4

test
```

- GET with gzip encoding:
```plaintext
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Encoding: gzip
Content-Length: <compressed-size>

<gzip-compressed body>
```

- POST file upload response:
```plaintext
HTTP/1.1 201 Created
```

## Limitations
This server is intended for educational purposes and small-scale testing. It’s not recommended for production use due to the simplicity of its error handling and security model.

## Note
Head over to [codecrafters.io](https://codecrafters.io) to try the challenge yourself.
