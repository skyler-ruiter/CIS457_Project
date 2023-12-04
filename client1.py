import socket
import os


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = ''

    while message.lower().strip() != 'bye':
        data = client_socket.recv(1024).decode()  # receive response

        print(data)  # show in terminal
        
        if data == "Downloading file...":
            filename = input("Enter filename: ")
            if not os.path.exists(filename):
                print("File does not exist")
                continue
            
            with open(filename, 'rb') as f:
                filesize = os.stat(filename).st_size
                client_socket.send(filename.encode())
                client_socket.send(str(filesize).encode())
                data = client_socket.recv(1024).decode()
                
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.send(data)
            print("File sent")
            continue
        
        message = input(" -> ")  # again take input
        client_socket.send(message.encode())

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()