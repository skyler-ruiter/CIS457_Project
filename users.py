import hashlib
import secrets

# Dictionary to store user credentials (hashed passwords)
users = {}

def register_user(username, password):
    salt = secrets.token_hex(8)  # Generate a random salt
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    users[username] = {'salt': salt, 'hashed_password': hashed_password}

def login_user(username, password):
    if username not in users:
        return False

    salt = users[username]['salt']
    hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    return hashed_password == users[username]['hashed_password']

def generate_token():
    return secrets.token_hex(32)  # Generate a random authentication token

# method to download users to a file
def download_users():
    with open('users.txt', 'w') as f:
        for user in users:
            f.write(user + '\n')
            f.write(users[user]['salt'] + '\n')
            f.write(users[user]['hashed_password'] + '\n')

# method to upload users from a file
def upload_users():
    global users
    users = {}
    with open('users.txt', 'r') as f:
        while True:
            username = f.readline().strip()
            if not username:
                break
            salt = f.readline().strip()
            hashed_password = f.readline().strip()
            users[username] = {'salt': salt, 'hashed_password': hashed_password}
