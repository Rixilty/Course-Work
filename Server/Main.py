import socket
import threading
import sqlite3

class Server:

    def __init__(self):
        self.host = "localhost"
        self.port = 5000
        self.database = "logins.db"
        self.message_db = "messages.db"

    def parse_request(self, data):
        # Parse /s:username:password, /l:username:password, /lo:user, /sc:user:status, /get
        try:
            data = data.strip()
            if not data.startswith("/"):
                return None, None, None, "Invalid format"

            parts = data.split(":")
            command = parts[0]

            if command == "/s":
                return "signup", parts[1], parts[2], None
            elif command == "/l":
                return "login", parts[1], parts[2], None
            elif command == "/lo":
                return "logout", parts[1], None, None
            elif command == "/sc":
                return "status_change", parts[1], parts[2], None
            elif command == "/get":
                return "get_status", None, None, None
            else:
                return None, None, None, f"Unknown command: {command}"

        except Exception as e:
            return None, None, None, f"Parse error: {str(e)}"

    def handle_client(self, client_socket, address):
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            print(f"Received from {address}: {data}")

            action, part1, part2, error = self.parse_request(data)

            if error:
                response = f"ERROR: {error}"
            elif action == "signup":
                response = self.signup(part1, part2)
            elif action == "login":
                response = self.login(part1, part2)
            elif action == "logout":
                response = self.logout(part1)
            elif action == "status_change":
                response = self.status_change(part1, part2) # forgot part2 for new_status
            elif action == "get_status":
                response = self.get_list()
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
        try:
            # Open the database
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()

            # Insert into table
            cursor.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, password))

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
            cursor.execute("SELECT * FROM logins WHERE username = ? AND password = ?", (username, password))

            user = cursor.fetchone()

            # If the user is found
            if user:
                # Increase login_count by 1 and set status to online
                cursor.execute("UPDATE logins SET login_count = login_count + 1, status = 'online' WHERE username = ?", (username,))
                conn.commit()
                conn.close()
                return f"SUCCESS: Login successful for {username}"
            # Else if user is not found
            else:
                conn.close()
                return f"ERROR: Invalid username or password"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def logout(self, username):
        # This will change the counter that tells us how many devices is logged into an account at once
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            # Remove 1 from devices but don't go below 0
            cursor.execute("UPDATE logins SET login_count = MAX(0, login_count - 1) WHERE username = ?", (username,))

            # Check if any devices are left
            cursor.execute("SELECT login_count FROM logins WHERE username = ?", (username,))
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("UPDATE logins SET status = 'offline' WHERE username = ?", (username,))

            conn.commit()
            conn.close()
            return f"SUCCESS: Logout successful for {username}"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def status_change(self, username, new_status):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            # Change the status column
            cursor.execute("UPDATE logins SET status = ? WHERE username = ?", (new_status, username))
            conn.commit()
            conn.close()
            return f"SUCCESS: Status updated successfully for {username} to {new_status}"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def get_list(self):
        try:
            conn = sqlite3.connect(self.database)
            cursor = conn.cursor()
            cursor.execute("SELECT username, status FROM logins")
            rows = cursor.fetchall()
            conn.close()
            print(f"DEBUG: get_list found {len(rows)} rows")

            if not rows:
                return "ERROR: No users found"

            # Making a string in this format user1:online,user2:offline
            user_list = []
            for name, status in rows:
                # Making sure there's no spaces in the format for better parsing
                user_list.append(f"{name}:{status}")

            return ",".join(user_list) # Better way to join with commas
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