import socket
import threading
import sqlite3

class Server:

    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.database = "logins.db"

    def parse_request(self, data):
        # Parse /s:username:password or /l:username:password
        try:
            data = data.strip()
            if not data.startswith("/"):
                return None, None, None, "Invalid format"

            parts = data.split(":")
            if len(parts) != 3:
                return None, None, None, "Invalid format"

            command = parts[0]
            username = parts[1]
            password = parts[2]

            if command == "/s":
                action = "signup"
            elif command == "/l":
                action = "login"
            else:
                return None, None, None, f"Unknown command: {command}"

            return action, username, password, None

        except Exception as e:
            return None, None, None, f"Parse error: {str(e)}"

    def handle_client(self, client_socket, address):
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            print(f"Received from {address}: {data}")

            action, username, password, error = self.parse_request(data)

            if error:
                response = f"Error: {error}"
            elif action == "signup":
                response = self.signup(username, password)
            elif action == "login":
                response = self.login(username, password)
            else:
                response = "ERROR: Invalid action"

            print(f"Sending response: {response}")
            client_socket.send(response.encode("utf-8"))

        except Exception as e:
            response = f"ERROR: {str(e)}"
            client_socket.send(response.encode("utf-8"))
        finally:
            client_socket.close()

    def signup(self, username, password):
        # Add a user to the database
            # Open the database
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()

            # Insert into table
            cursor.execute(f"INSERT INTO users (username, password) VALUES ({username}, {password})")

            # Save changes and close the database
            conn.commit()
            conn.close()
            return f"SUCCESS: User {username} created"
        # If username already exists
        except sqlite3.IntegrityError:
            return f"ERROR: User {username} already exists"
        # Other errors
        except Exception as e:
            return f"ERROR: {str(e)}"

    def login(self, username, password):
        # Check if the user exists in the database
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()

            # Find a match from the table
            cursor.execute(f"SELECT * FROM users WHERE username = {username} AND password = {password}")

            user = cursor.fetchone()
            conn.close()

            # If the user is found
            if user:
                return f"SUCCESS: Login successful for {username}"
            # Else if user is not found
            else:
                return f"ERROR: Invalid username or password"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, address = server_socket.accept()
            print(f"New connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    server = Server()
    server.start()