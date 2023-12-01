import socket
import threading

def handle_client(client_socket, client_address, other_client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Send the received message to the other client
            other_client_socket.send(data)
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"Server listening on {host}:{port}")

    clients = []

    try:
        while len(clients) < 2:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Add the client to the list of connected clients
            clients.append((client_socket, client_address))

            # If two clients are connected, start a new thread for each client
            if len(clients) == 2:
                thread1 = threading.Thread(target=handle_client, args=(clients[0][0], clients[0][1], clients[1][0]))
                thread2 = threading.Thread(target=handle_client, args=(clients[1][0], clients[1][1], clients[0][0]))

                thread1.start()
                thread2.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
