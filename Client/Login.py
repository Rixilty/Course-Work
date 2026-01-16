import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


class Login_GUI:

    def __init__(self):

        self.root = ctk.CTk()
        self.window_width = 550
        self.window_height = 420

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.title("Login")
        self.root.configure(fg_color="#1c1c1c")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1c1c1c")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=0)

        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c") # Fixed frame
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10,5))
        self.top_frame.grid_columnconfigure(0, weight=1)

        self.Title = ctk.CTkLabel(self.top_frame, text="Login", font=("Arial", 31, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Title.grid(row=0, column=0, columnspan=2, sticky="n", pady=10)

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c")
        self.content_frame.grid(row=1, column=0, sticky="")
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=0)

        self.Username_label = ctk.CTkLabel(self.content_frame, text="Username:", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Username_label.grid(row=1, column=0, sticky="e", padx=(0,10))

        self.Username_entry = ctk.CTkEntry(self.content_frame, width=250, font=("Arial", 12), placeholder_text="Username", fg_color="white", text_color="black", placeholder_text_color="grey")
        self.Username_entry.grid(row=1, column=1, pady=5)

        self.Password_label = ctk.CTkLabel(self.content_frame, text="Password:", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Password_label.grid(row=3, column=0, sticky="e", padx=(0,10))

        self.Password_entry = ctk.CTkEntry(self.content_frame, width=250, font=("Arial", 12), show="*", placeholder_text="Password", fg_color="white", text_color="black", placeholder_text_color="grey")
        self.Password_entry.grid(row=3, column=1, pady=5)

        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=0)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        self.Login_button = ctk.CTkButton(self.bottom_frame, text="Login", fg_color="#1c1c1c", text_color="white", hover_color="#282828", border_width=1, border_color="#424242", font=("Arial", 14, "bold"), command=self.Login)
        self.Login_button.grid(row=5, column=0, columnspan=2, sticky="n", pady=(10,0))

        self.error_label = ctk.CTkLabel(self.main_frame, text="", text_color="red", fg_color="#1c1c1c", font=("Arial", 14, "bold"))
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(10,0))

        self.not_signed_label = ctk.CTkLabel(self.bottom_frame, text="Don't have an account?", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.not_signed_label.grid(row=0, column=0, sticky="e")

        self.signup_link = ctk.CTkLabel(self.bottom_frame, text="Sign up.", font=("Arial",13, "bold", "underline"), text_color="#001eff", fg_color="#1c1c1c", cursor="hand2")
        self.signup_link.grid(row=0, column=1, padx=0, sticky="w")

        self.signup_link.bind("<Button-1>", self.on_signup_click)

        self.username_requirements_frame = ctk.CTkFrame(self.content_frame, fg_color="#1c1c1c")
        self.username_requirements_frame.grid(row=2, column=1, sticky="w", pady=(5,0))

        self.username_length_requirement = ctk.CTkLabel(self.username_requirements_frame, text="● Username Length Must Be Between 3-16", text_color="red")

        self.username_length_requirement.pack(anchor="w")

        self.username_requirements_frame.grid_remove()

        self.Username_entry.bind("<FocusIn>", lambda e: self.username_requirements_frame.grid())
        self.Username_entry.bind("<FocusOut>", lambda e: self.username_requirements_frame.grid_remove())

        self.Username_entry.bind("<KeyRelease>", self.check_username_requirements)

        self.password_requirements_frame = ctk.CTkFrame(self.content_frame, fg_color="#1c1c1c")
        self.password_requirements_frame.grid(row=4, column=1, sticky="w", pady=(5,0))

        self.uppercase_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Uppercase Letter", text_color="red")
        self.lowercase_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Lowercase Letter", text_color="red")
        self.digit_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Number", text_color="red")
        self.symbol_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Symbol", text_color="red")
        self.password_length_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● Password Length Must Be Between 8-16", text_color="red")

        self.uppercase_requirement.pack(anchor="w")
        self.lowercase_requirement.pack(anchor="w")
        self.digit_requirement.pack(anchor="w")
        self.symbol_requirement.pack(anchor="w")
        self.password_length_requirement.pack(anchor="w")

        self.password_requirements_frame.grid_remove()

        self.Password_entry.bind("<FocusIn>", lambda e: self.password_requirements_frame.grid())
        self.Password_entry.bind("<FocusOut>", lambda e: self.password_requirements_frame.grid_remove())

        self.Password_entry.bind("<KeyRelease>", self.check_password_requirements)

        self.root.mainloop()

    def Login(self):
        Username = self.Username_entry.get()
        Password = self.Password_entry.get()
        self.error_label.configure(text="", text_color="red")

        if Username == "" or Password == "":
            self.error_label.configure(text="Fill in all fields!")

        elif self.username_length_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Username must be 3-16 characters!")

        elif self.uppercase_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Password must contain at least one uppercase letter!")

        elif self.lowercase_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Password must contain at least one lowercase letter!")

        elif self.digit_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Password must contain at least one number!")

        elif self.symbol_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Password must contain at least one symbol!")

        elif self.password_length_requirement.cget("text_color") == "red":
            self.error_label.configure(text="Password must be 8-16 characters!")

        else:
            self.error_label.configure(text="Login Successful!", text_color="green")

    def on_signup_click(self, event):
        pass

    def check_password_requirements(self, event=None):
        Password = self.Password_entry.get()

        for i in [self.password_length_requirement, self.uppercase_requirement, self.lowercase_requirement, self.digit_requirement, self.symbol_requirement]:
            i.configure(text_color="red")

        if len(Password) > 8 and len(Password) < 16:
            self.password_length_requirement.configure(text_color="green")

        for i in Password:
            if i.isupper():  # Checks for uppercase letters
                self.uppercase_requirement.configure(text_color="green")
            if i.islower():  # Checks for lowercase letters
                self.lowercase_requirement.configure(text_color="green")
            if i.isdigit():  # Checks for numbers
                self.digit_requirement.configure(text_color="green")
            if not i.isalnum():  # Checks for symbols
                self.symbol_requirement.configure(text_color="green")

    def check_username_requirements(self, event=None):
        Username = self.Username_entry.get()

        self.username_length_requirement.configure(text_color="red")

        if len(Username) > 2 and len(Username) < 16:
            self.username_length_requirement.configure(text_color="green")

Login_GUI()