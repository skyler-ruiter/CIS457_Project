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
        
        if data == "Download" or data == "Upload":
            filename = input("Enter filename: ")
            if not os.path.exists(filename):
                # make the file
                open(filename, 'w').close()
            
            if data == "Download":
                client_socket.send(filename.encode())
                filesize = int(client_socket.recv(1024).decode())
                client_socket.send("File received".encode())
                with open(filename, 'wb') as f:
                        while filesize > 0:
                            data = b''
                            if filesize < 1024:
                                data = client_socket.recv(filesize)
                            else:
                                data = client_socket.recv(1024)
                            f.write(data)
                            filesize -= len(data)
                print("File received")
            else:
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
        
        if data == "Registration successful" or \
           data == "Login successful" or \
           data == "Logout successful" or \
           data == "File received" or \
           data == "List":
            continue
        
        message = input(" -> ")  # again take input
        client_socket.send(message.encode())

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()