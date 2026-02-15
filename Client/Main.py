import socket
from tkinter import mainloop
import customtkinter as ctk
import time
import tkinter as tk

class MessagingApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.username = username # Getting the user's username
        self.title("Messaging App")
        self.geometry("1000x600")
        self.configure(fg_color="#1c1c1c")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Status
        self.current_status = "online"
        self.last_activity = time.time()
        self.idle_timeout = 300 # 5 minutes
        self.status_check_interval = 30
        self.my_status_dot = None

        self.setup_sidebar()
        self.setup_chat_window()

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # This tells use when the user hits the "X" to exit the program

        self._refresh_after_id = None
        self.refresh_sidebar()

        # Start idle checker
        self.check_idle_status()

        # Bind events
        self.bind_all("<Key>", self.on_activity)
        self.bind_all("<Button>", self.on_activity)
        self.bind_all("<Motion>", self.on_activity)

    def setup_sidebar(self):
        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1c1c1c")
        self.sidebar.grid(row=0, column=1, sticky="nsew")

        # Scrollable frame for user list
        self.user_list_frame = ctk.CTkScrollableFrame(self.sidebar, width=200, label_text="Users", label_font=("Arial", 16, "bold"))
        self.user_list_frame.pack(side="left", fill="y", padx=10, pady=(20,10))

    def setup_chat_window(self):
        # Main Chat Container
        self.chat_container = ctk.CTkFrame(self, fg_color="#1c1c1c")
        self.chat_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_container.rowconfigure(0, weight=1)
        self.chat_container.columnconfigure(0, weight=1)

        # Message display box
        self.message_display = ctk.CTkTextbox(self.chat_container, corner_radius=10, font=("Arial", 14))
        self.message_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.message_display.configure(state="disabled")

        # Input Area
        self.input_frame = ctk.CTkFrame(self.chat_container, fg_color="#1c1c1c")
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.entry_message = ctk.CTkEntry(self.input_frame, placeholder_text="Send a message...", height=40)
        self.entry_message.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.send_button = ctk.CTkButton(self.input_frame, text="➤", width=50, height=40, command=self.send_action)
        self.send_button.grid(row=0, column=1)

    def add_user_to_sidebar(self, username, status):
        colors = {"online": "green", "away": "yellow", "offline": "red"}
        color = colors.get(status.lower(), "grey")

        user_row = ctk.CTkFrame(self.user_list_frame, fg_color="#1c1c1c")
        user_row.pack(fill="x", pady=2)

        status_dot = ctk.CTkLabel(user_row, text="●", text_color=color, font=("Arial", 18))
        status_dot.pack(side="left", padx=5)

        if username == self.username:
            self.my_status_dot = status_dot
            name_label = ctk.CTkLabel(user_row, text=username, font=("Arial", 18, "bold")) # Highlight own name
        else:
            name_label = ctk.CTkLabel(user_row, text=username, font=("Arial", 18))

        name_label.pack(side="left")

        if username == self.username:
            self.my_user_row = user_row
            self.my_status_dot = status_dot
            # Bind right click to the row and its children
            user_row.bind("<Button-3>", self.show_status_menu)
            status_dot.bind("<Button-3>", self.show_status_menu)
            name_label.bind("<Button-3>", self.show_status_menu)

    def send_action(self):
        message = self.entry_message.get()
        print("Sending...",message)

        # Temporary display logic for testing
        self.message_display.configure(state="normal")
        self.message_display.insert("end", f"You: {message}\n")
        self.message_display.configure(state="disabled")
        self.message_display.see("end")

        self.entry_message.delete(0, "end")

    def refresh_sidebar(self):
        # Cancel any previously scheduled refresh
        if self._refresh_after_id:
            self.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        # This sends the command /get to the server and updates the status for all users
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2)
            client.connect(("localhost", 5000))

            # Send /get
            client.send("/get".encode("utf-8"))
            response = client.recv(1024).decode("utf-8")
            print(f"DEBUG: refresh_side_bar received: {response}")
            client.close()

            if not response.startswith("ERROR"):
                # Clear current sidebar widgets
                for i in self.user_list_frame.winfo_children():
                    i.destroy()

                # Parse "user1:online,user2:away,user3:offline,etc"
                users = response.split(",")
                users_list = []
                for i in users:
                    if ":" in i:
                        name, status = i.split(":")
                        # Create a label for each user
                        self.add_user_to_sidebar(name, status)
                # Sort so that the user always appears firt
                yourself = None
                others = []
                for name, status in users_list:
                    if name == self.username:
                        yourself = (name, status)
                    else:
                        others.append((name, status))

                sorted_users = []
                if yourself:
                    sorted_users.append(yourself)
                sorted_users.extend(others)

                for name, status in sorted_users:
                    self.add_user_to_sidebar(name, status)

        except Exception as e:
            # Printing traceback for debugging
            import traceback
            traceback.print_exc()
            print(f"Sidebar sync failes: {e}")
        finally:
            # Schedule the next refresh only after this one is completed
            self._refresh_after_id = self.after(3000, self.refresh_sidebar)

    def on_closing(self):
        # This tells the server to -1 from login_count (1 less device is on the account) before exiting
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 5000))
            client.send(f"/lo:{self.username}".encode("utf-8"))
            client.close()
        except:
            pass # Incase the server is down
        self.destroy()

    def on_activity(self, event=None):
        # Called whenever the user interacts with the app
        self.last_activity = time.time()

        # If the user was away and becomes active, set back to online
        if self.current_status == "away":
            self.update_status("online")

    def check_idle_status(self):
        # Check if the user has been idle and update the status to away if so
        idle_time = time.time() - self.last_activity

        if idle_time > self.idle_timeout and self.current_status == "online":
            self.update_status("away")

    def update_status(self, new_status):
        # Update local status and notify server
        if new_status == self.current_status:
            return

        self.current_status = new_status
        print(f"Status changed to: {new_status}")

        colors = {"online": "green", "away": "yellow", "offline": "red"}
        if self.my_status_dot:
            self.my_status_dot.configure(text_color=colors.get(new_status, "grey"))

        self.send_status_to_server(new_status)

    def send_status_to_server(self, status):
        # Send status change to server in the format --> /sc:username:status
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2)
            client.connect(("localhost", 5000))

            # Format --> /sc:username:status
            command = f"/sc:{self.username}:{status}"
            client.send(command.encode("utf-8"))

            response = client.recv(1024).decode("utf-8")
            client.close()

            if response.startswith("SUCCESS"):
                print(f"Status update successful: {response}")
            else:
                print(f"Status update failed: {response}")

        except Exception as e:
            print(f"Failed to send status update: {e}")

    def show_status_menu(self, event):
        # A popup menu to change status on right click
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Online", command=lambda: self.update_status("online"))
        menu.add_command(label="Away", command=lambda: self.update_status("away"))
        menu.add_command(label="Offline", command=lambda: self.update_status("offline"))
        menu.config(bg="#1c1c1c", fg="white", activebackground="#333333", activeforeground="white", font=("Arial", 12))
        menu.tk_popup(event.x_root, event.y_root)


if __name__ == "__main__":
    app = MessagingApp("TEST")
    # Removed users for testing
    app.mainloop()
