import socket
import users


def server_program():
    logged_in = False
    host = socket.gethostname()
    port = 5000
    users.upload_users()
    
    server_socket = socket.socket()
    server_socket.bind((host, port))

    # how many clients the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Welcome to the Data Archiver and Transport Application (DATA)")
    print("Connection from: " + str(address))
    
    # ask the client whether he wants to login or register
    message = 'Login or Register?'
    conn.send(message.encode())
    
    while not logged_in:
        
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            return
    
        if data == 'Register':
            message = 'Enter new username: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                return
            username = data
            message = 'Enter new password: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                return
            password = data
            users.register_user(username, password)
            message = 'Registration successful'
            conn.send(message.encode())
            
            users.download_users()
            
            if users.login_user(username, password):
                message = 'Login successful'
                conn.send(message.encode())
                logged_in = True
            else:
                message = 'Login failed'
                conn.send(message.encode())
                return
            
        else:
            message = 'Enter username: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                return
            username = data
            message = 'Enter password: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                return
            password = data
            if users.login_user(username, password):
                message = 'Login successful'
                conn.send(message.encode())
                logged_in = True
            else:
                message = 'Login failed'
                conn.send(message.encode())
                return
    
    
    while True:
    
        # now that the user is logged in, ask them what they want to do
        message = '\nWhat would you like to do?'
        conn.send(message.encode())
    
        if not logged_in:
            return
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            return
        if data == 'Upload':
            message = 'Downloading file...'
            conn.send(message.encode())
            
            
            filename = conn.recv(1024).decode()
            if not filename:
                # if data is not received break
                return
            # receive the file into the user's directory
            filelocation = 'users/' + username + '/' + filename
            
            filesize = conn.recv(1024).decode()
            
            with open(filelocation, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
                
            
            message = 'File received'
            conn.send(message.encode())
            
            # add the file to the user's list of files
            users.add_file(username, filename)
            
            break
            


    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()