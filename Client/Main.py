from tkinter import mainloop

import customtkinter as ctk

class MessagingApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()

        self.title("Messaging App")
        self.geometry("1000x600")
        self.configure(fg_color="#1c1c1c")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_chat_window()

    def setup_sidebar(self):
        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1c1c1c")
        self.sidebar.grid(row=0, column=1, sticky="nsew")

        # This holds user status rows
        self.user_label = ctk.CTkLabel(self.sidebar, text="USERS", font=("Arial", 16, "bold"))
        self.user_label.pack(pady=20, padx=10)

        # Scrollable frame for user list
        self.user_list_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="#1c1c1c")
        self.user_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

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
        colors = {"online": "GREEN", "away": "YELLOW", "offline": "RED"}
        color = colors.get(status.lower(), "GREY")

        user_row = ctk.CTkFrame(self.user_list_frame, fg_color="#1c1c1c")
        user_row.pack(fill="x", pady=2)

        status_dot = ctk.CTkLabel(user_row, text="●", text_color=color, font=("Arial", 18))
        status_dot.pack(side="left", padx=5)

        name_label = ctk.CTkLabel(user_row, text=username)
        name_label.pack(side="left")

    def send_action(self):
        message = self.entry_message.get()
        print("Sending...",message)

        # Temporary display logic for testing
        self.message_display.configure(state="normal")
        self.message_display.insert("end", f"You: {message}\n")
        self.message_display.configure(state="disabled")
        self.message_display.see("end")

        self.entry_message.delete(0, "end")

if __name__ == "__main__":
    app = MessagingApp("TEST")
    # Adding more users for testing
    app.add_user_to_sidebar("User1", "online")
    app.add_user_to_sidebar("User2", "away")
    app.add_user_to_sidebar("User3", "offline")
    app.mainloop()
