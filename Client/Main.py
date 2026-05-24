import os
import socket
import sqlite3
import threading
import customtkinter as ctk
import time
import tkinter as tk
from cryptography.fernet import Fernet
from Translator import translate_text, translate_message
from googletrans import LANGUAGES
from tkinter import messagebox

SECURITY_KEY = b'HbQ3dWJrZQ-mkWA65QPoebyExSqK6fy-dljZxbRDdE4='
cipher_suite = Fernet(SECURITY_KEY)

DARK_THEME = {
    "bg": "#1c1c1c",
    "text1": "white",
    "hover": "#282828",
    "border": "#424242"
}

LIGHT_THEME = {
    "bg": "#f0f0f0",
    "text1": "black",
    "hover": "#e0e0e0",
    "border": "#cccccc"
}

THEME = DARK_THEME

class MessagingApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.username = username # Getting the user's username
        self.lang_map = {}
        for code, name in LANGUAGES.items():
            self.lang_map[name.title()] = code

        global THEME
        THEME = self.load_theme_config()

        self.title("Messaging App")
        self.geometry("1000x600")
        self.configure(fg_color=THEME["bg"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Setting up the UI but keeping it hidden
        self.setup_sidebar()
        self.setup_chat_window()

        # Loading screen
        self.loading_frame = ctk.CTkFrame(self, fg_color=THEME["bg"])
        self.loading_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.loading_label = ctk.CTkLabel(self.loading_frame, text=translate_text("Retrieving messages from server...\nPlease wait a moment."), font=("Arial", 20, "bold"))
        self.loading_label.pack(expand=True)

        # Initialize database
        self.init_db()

        threading.Thread(target=self.load_local_history, daemon=True).start()

        self.after(0, self.finish_loading)

        # Status
        self.current_status = "online"
        self.last_activity = time.time()
        self.idle_timeout = 300 # 5 minutes
        self.status_check_interval = 30
        self.my_status_dot = None

        # Message tracking
        self.last_message_id = 0
        self.fetch_after_id = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # This tells use when the user hits the "X" to exit the program

        self._refresh_after_id = None

        # Bind events
        self.bind_all("<Key>", self.on_activity)
        self.bind_all("<Button>", self.on_activity)
        self.bind_all("<Motion>", self.on_activity)

        # Track translation toggle
        self.translate_on = True
        self._refresh_after_id = None

    def load_theme_config(self):
        mode = "dark" #default
        try:
            if os.path.exists("theme_config.txt"):
                with open("theme_config.txt", "r") as f:
                    mode = f.read().strip().lower()
                    if mode == "light":
                        self.current_theme_mode = "light"
                        ctk.set_appearance_mode("light")
                        return LIGHT_THEME
            self.current_theme_mode = "dark"
            ctk.set_appearance_mode("dark")
            return DARK_THEME
        except:
            self.current_theme_mode = "dark"
            return DARK_THEME

    def init_db(self):
        # Creating a local SQLite database for the user if it doesn't exist. This will store message ID, sender, original message, translated message and timestamp
        self.conn = sqlite3.connect(f"chat_history_{self.username}.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY,
            sender TEXT,
            original_message TEXT,
            translated_message TEXT,
            timestamp TEXT
            )
        ''')
        self.conn.commit()

    def load_local_history(self):
        # This will laod cached messages from the database on startup
        self.cursor.execute("SELECT id, sender, translated_message, timestamp FROM chat_history ORDER BY id ASC")
        rows = self.cursor.fetchall()

        if not rows:
            self.last_message_id = 0
            return

        self.last_message_id = max(row[0] for row in rows)

        def process_batch(index=0):
            batch_size = 25 # Number of messages per batch
            self.message_display.configure(state="normal")

            end_index = min(index + batch_size, len(rows))
            for i in range(index, end_index):
                id, sender, translated_message, timestamp = rows[i]
                self.display_message(sender, translated_message, timestamp)

            self.message_display.configure(state="disabled")
            self.message_display.see("end")

            # If there are more messages, schedule the next batch after a tiny delay
            if end_index < len(rows):
                self.after(10, lambda: process_batch(end_index))

        self.after(10, lambda: process_batch(0))

    def finish_loading(self):
        # Remove the loading screen
        self.loading_frame.destroy()
        self.message_display.see("end")

        # Now start tge live background syncs
        self.refresh_sidebar()
        self.fetch_messages()
        self.check_idle_status()

    def save_message_to_db(self, id, sender, original, translated, timestamp):
        # This saves a new message locally
        try:
            self.cursor.execute('''
            INSERT OR IGNORE INTO chat_history (id, sender, original_message, translated_message, timestamp)
            VALUES (?,?,?,?,?)
            ''', (id, sender, original, translated, timestamp))
            self.conn.commit()
        except Exception as e:
            print(f"DB Save Error: {e}")

    def setup_sidebar(self):
        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=THEME["bg"])
        self.sidebar.grid(row=0, column=1, sticky="nsew")

        # Scrollable frame for user list
        self.user_list_frame = ctk.CTkScrollableFrame(self.sidebar, width=200, label_text=translate_text("Users"), label_font=("Arial", 16, "bold"))
        self.user_list_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(20,10))

        # Settings button
        self.settings_button = ctk.CTkButton(self.sidebar, text=("⚙️", translate_text("Settings")), command=self.open_settings, text_color=THEME["text1"], fg_color=THEME["hover"], hover_color=THEME["border"])
        self.settings_button.pack(side="bottom", padx=10, pady=20)

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self) # Places the settings menu on top when it opens so the user can see it
        settings_window.title("Settings")
        settings_window.geometry("500x500")
        settings_window.attributes("-topmost", True) # Keeps on top

        ctk.CTkLabel(settings_window, text=translate_text("Theme"), font=("Arial", 14, "bold")).pack(pady=(20,5))

        # Switch theme
        theme_menu = ctk.CTkOptionMenu(settings_window, values=["Dark", "Light"], command=self.change_theme)
        theme_menu.set(self.current_theme_mode.title())
        theme_menu.pack(pady=10)

        # Translation toggle section
        ctk.CTkLabel(settings_window, text=translate_text("Translation"), font=("Arial", 14, "bold")).pack(pady=(20,5))

        self.trans_switch = ctk.CTkSwitch(
            settings_window,
            text=translate_text("Auto translate messages"),
            command=self.toggle_translation
        )

        # Switch to match current state
        if self.translate_on:
            self.trans_switch.select()
        self.trans_switch.pack(pady=10)

        ctk.CTkLabel(settings_window, text=translate_text("Language"), font=("Arial", 14, "bold")).pack(pady=(20,5))
        # Language menu moved here
        lang_names = sorted(list(self.lang_map.keys()))
        self.lang_menu = ctk.CTkOptionMenu(settings_window, values=lang_names, command=self.change_language_event)

        try:
            with open("config.txt", "r") as f:
                current_code = f.read().strip().lower()
                self.lang_menu.set(LANGUAGES.get(current_code, "english").title())
        except:
            self.lang_menu.set("English")

        self.lang_menu.pack(pady=10)

    def toggle_translation(self):
        self.translate_on = self.trans_switch.get() == 1
        if self.translate_on:
            state = "Enabled"
        else:
            state = "Disabled"

    def change_theme(self, new_mode):
        mode = new_mode.lower()
        with open("theme_config.txt", "w") as f:
            f.write(new_mode)

        messagebox.showinfo("Theme Changed", "Theme preference saved. Please restart the app to apply all the UI changes")

    def setup_chat_window(self):
        # Main Chat Container
        self.chat_container = ctk.CTkFrame(self, fg_color=THEME["bg"])
        self.chat_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.chat_container.rowconfigure(0, weight=1)
        self.chat_container.columnconfigure(0, weight=1)

        # Message display box
        self.message_display = ctk.CTkTextbox(self.chat_container, corner_radius=10, font=("Arial", 14))
        self.message_display.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.message_display.configure(state="disabled")

        # Input Area
        self.input_frame = ctk.CTkFrame(self.chat_container, fg_color=THEME["bg"])
        self.input_frame.grid(row=1, column=0, sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.entry_message = ctk.CTkEntry(self.input_frame, placeholder_text=translate_text("Send a message..."), height=40)
        self.entry_message.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        # Enter key binding
        self.entry_message.bind("<Return>", lambda event: self.send_action())

        self.send_button = ctk.CTkButton(self.input_frame, text="➤", width=50, height=40, command=self.send_action)
        self.send_button.grid(row=0, column=1)

    def add_user_to_sidebar(self, username, status):
        colors = {"online": "green", "away": "yellow", "offline": "red"}
        color = colors.get(status.lower(), "grey")

        user_row = ctk.CTkFrame(self.user_list_frame, fg_color=THEME["bg"])
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
        message = self.entry_message.get().strip()
        if not message:
            return
        print("Sending...",message)

        # Instantly display the user's message on the screen
        time_string = time.strftime("%H:%M:%S")
        self.display_message(translate_text("You"), message, time_string)
        self.entry_message.delete(0, "end")

        # Run encryption and networking in the background on a different thread
        def background_send():
            try:
                # Encryption
                encrypted_bytes = cipher_suite.encrypt(message.encode("utf-8"))
                encrypted_message = encrypted_bytes.decode("utf-8")
                message_length = len(encrypted_message)

                # Networking
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(3)
                client.connect(("82.30.29.190", 19134))
                command = f"/m:{self.username}:{message_length}:{encrypted_message}"
                client.send(command.encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                client.close()

                if response.startswith("SUCCESS"):
                    try:
                        # Extract the new id the server gave us and save it to the DB
                        new_id = int(response.split(":")[1].strip())
                        self.save_message_to_db(new_id, self.username, message, message, time_string)
                        if new_id > self.last_message_id:
                            self.last_message_id = new_id
                    except:
                        pass
                    print("Message sent successfully")
                else:
                    print(f"Message sent failed: {response}")
            except Exception as e:
                print(e)
        threading.Thread(target=background_send, daemon=True).start()


    def refresh_sidebar(self):
        # Cancel any previously scheduled refresh
        if self._refresh_after_id:
            self.after_cancel(self._refresh_after_id)
            self._refresh_after_id = None
        # This sends the command /get to the server and updates the status for all users
        def background_refresh():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(2)
                client.connect(("82.30.29.190", 19134))

                # Send /get
                client.send("/get".encode("utf-8"))
                response = client.recv(1024).decode("utf-8")
                print(f"DEBUG: refresh_side_bar received: {response}")
                client.close()

                if not response.startswith("ERROR"):
                    # Safely pass the user data to the Main Thread
                    self.after(0, lambda: self.update_sidebar_ui(response))
            except Exception as e:
                # Printing traceback for debugging
                import traceback
                traceback.print_exc()
                print(f"Sidebar sync failes: {e}")
            finally:
                # Schedule the next refresh only after this one is completed
                self._refresh_after_id = self.after(3000, self.refresh_sidebar)
        threading.Thread(target=background_refresh, daemon=True).start()

    def update_sidebar_ui(self, response):
        # This redraws the UI on the main thread
        # Parse "user1:online||user2:away||user3:offline||etc"
        users = response.split("||")
        users_list = []
        for i in users:
            if ":" in i:
                name, status = i.split(":")
                # Create a label for each user
                users_list.append((name, status))
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
        for i in self.user_list_frame.winfo_children():
            i.destroy()
        for name, status in sorted_users:
            self.add_user_to_sidebar(name, status)

    def on_closing(self):
        # This tells the server to -1 from login_count (1 less device is on the account) before exiting
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("82.30.29.190", 19134))
            client.send(f"/lo:{self.username}".encode("utf-8"))
            client.close()
        except:
            pass # Incase the server is down
        if self._fetch_after_id:
            self.after_cancel(self._fetch_after_id)
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
        def background_status():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(2)
                client.connect(("82.30.29.190", 19134))

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
        threading.Thread(target=background_status, daemon=True).start()

    def show_status_menu(self, event):
        # A popup menu to change status on right click
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Online", command=lambda: self.update_status("online"))
        menu.add_command(label="Away", command=lambda: self.update_status("away"))
        menu.add_command(label="Offline", command=lambda: self.update_status("offline"))
        menu.config(bg=THEME["bg"], fg="white", activebackground="#333333", activeforeground="white", font=("Arial", 12))
        menu.tk_popup(event.x_root, event.y_root)

    def fetch_messages(self):
        # Fetch new messages from server and display them
        def background_fetch():
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(2)
                client.connect(("82.30.29.190", 19134))
                command = f"/fetch:{self.username}:{self.last_message_id}"
                client.send(command.encode("utf-8"))
                response = client.recv(1024*1024).decode("utf-8")
                client.close()

                print(f"DEBUG Response:{response}")

                if not response.startswith("ERROR") and not response.startswith("SUCCESS"):
                    self.after(0, lambda: self.process_incoming(response))
            except Exception as e:
                print(f"Fetch error: {e}")
            finally:
                self._fetch_after_id = self.after(3000, self.fetch_messages)
        threading.Thread(target=background_fetch, daemon=True).start()

    def process_incoming(self, response):
        # This runs on the Main Thread safely. It decrypts, translates, saves and displayes the message.
        messages = response.split("||")
        max_id = self.last_message_id

        for i in messages:
            if ":" in i:
                parts = i.split(":", 3)
                if len(parts) < 4:
                    continue

                message_id = int(parts[0])
                sender = parts[1]
                message_length = int(parts[2])

                max_id = max(max_id, message_id)

                # Skip if we already have the message, I did this because sometimes the server would sometimes randomly fetch older messages
                if message_id <= self.last_message_id:
                    continue

                remainder = parts[3]
                encrypted_message = remainder[:message_length]
                timestamp = remainder[message_length:].lstrip(":")

                try:
                    decrypted_bytes = cipher_suite.decrypt(encrypted_message.encode("utf-8"))
                    original_message = decrypted_bytes.decode("utf-8")
                except Exception as e:
                    continue

                if sender == self.username:
                    translated_msg = original_message
                elif self.translate_on:
                    translated_msg = translate_message(original_message)
                else:
                    translated_msg = original_message

                # Save to local database
                self.save_message_to_db(message_id, sender, original_message, translated_msg, timestamp)

                # Display it
                self.display_message(sender, translated_msg, timestamp)
                max_id = max(max_id, message_id)
        self.last_message_id = max_id

    def display_message(self, sender, message, timestamp=None):
        # Insert a message into the chat display
        time_string = ""
        if timestamp:
            # Extract HH:MM:SS from YYYY-MM-DD HH:MM:SS format
            if " " in timestamp:
                time_string = timestamp.split()[1]
            else:
                time_string = timestamp
            time_string = f"[{time_string}]"

        self.message_display.configure(state="normal")
        if sender in [self.username, translate_text("You")]:
            self.message_display.insert("end", f"{time_string} {translate_text("You")}:{message}\n")
        else:
            self.message_display.insert("end", f"{time_string} {sender}:{message}\n")
        self.message_display.configure(state="disabled")
        self.message_display.see("end")

    def change_language_event(self, selected_name):
        new_code = self.lang_map.get(selected_name)

        if new_code:
            try:
                with open("config.txt", "w") as f:
                    f.write(new_code)

                    messagebox.showinfo(translate_text("Language Changed"), f"Language set to {selected_name}. Please restart the app to apply UI changes.")
            except Exception as e:
                print(f"Failed to change language: {e}")

if __name__ == "__main__":
    app = MessagingApp("TEST")
    # Removed users for testing
    app.mainloop()