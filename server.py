import socket
import users
import os

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
    message = "Welcome to the Data Archiver and Transport Application (DATA) \nWould you like to Login or Register?"
    conn.send(message.encode())
    
    while not logged_in:
        
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            continue
    
        if data == 'Register':
            message = 'Enter new username: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                continue
            username = data
            message = 'Enter new password: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                continue
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
                continue
            
        else:
            message = 'Enter username: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                continue
            username = data
            message = 'Enter password: '
            conn.send(message.encode())
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                continue
            password = data
            if users.login_user(username, password):
                message = 'Login successful'
                conn.send(message.encode())
                logged_in = True
            else:
                message = 'Login failed'
                conn.send(message.encode())
                continue
    
    
    while True:
    
        # now that the user is logged in, ask them what they want to do
        message = '\nWhat would you like to do? (Upload, Download, List, Quit)'
        conn.send(message.encode())
    
        if not logged_in:
            break
        
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            data = ''
            continue
        
        
        if data == 'Upload':
            message = 'Upload'
            conn.send(message.encode())
            
            filename = conn.recv(1024).decode()
            if not filename:
                # if data is not received break
                return
            # receive the file into the user's directory
            filelocation = 'users/' + username + '/' + filename
            
            filesize = conn.recv(1024).decode()
            
            message = 'Metadata received'
            conn.send(message.encode())

            # receive the data into a variable first
            data = b''
            while True:
                packet = conn.recv(1024)
                # message = 'File piece received'
                # conn.send(message.encode())
                data += packet
                if len(data) >= int(filesize):
                    break
            # write the data to the file
            with open(filelocation, 'wb') as f:
                f.write(data)
            
            message = 'File received'
            conn.send(message.encode())
            
            # add the file to the user's list of files
            users.add_file(username, filename)
            users.download_user_files()
            data = 'Upload'
        elif data == 'Download':
            message = 'Download'
            conn.send(message.encode())
            
            filename = conn.recv(1024).decode()
            if not filename:
                # if data is not received break
                return
            # send the file from the user's directory
            filelocation = 'users/' + username + '/' + filename
            
            filesize = str(os.stat(filelocation).st_size)
            conn.send(filesize.encode())
            filesize = int(filesize)
            
            # send the data in chunks
            with open(filelocation, 'rb') as f:
                while filesize > 0:
                    data = b''
                    if filesize < 1024:
                        data = f.read(filesize)
                    else:
                        data = f.read(1024)
                    conn.send(data)
                    filesize -= len(data)
            
            message = 'File sent'
            conn.send(message.encode())
            data = 'Download'
        elif data == 'Quit':
            message = 'Goodbye'
            conn.send(message.encode())
            break
        elif data == 'List':
            users.upload_users()
            message = 'List\n'
            conn.send(message.encode())
            
            # send the list of files
            files = users.user_files[username]
            message = ''
            for file in files:
                message += file + '\n'
            conn.send(message.encode())
        else: 
            # send that they selected an invalid option
            message = 'Invalid option'
            conn.send(message.encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()