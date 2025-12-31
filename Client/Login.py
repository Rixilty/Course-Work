import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


class Login_GUI:

    def __init__(self):

        window_width = 500
        window_height = 350

        self.root = ctk.CTk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.title("Login")
        self.root.configure(fg_color="#1c1c1c")

        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1c1c1c")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.Title = ctk.CTkLabel(self.main_frame, text="Login", font=("Arial", 31, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Title.grid(row=0, column=0, columnspan=2, pady=20)

        self.Username_label = ctk.CTkLabel(self.main_frame, text="Username:", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Username_label.grid(row=1, column=0, sticky="e")

        self.Username_entry = ctk.CTkEntry(self.main_frame, width=250, font=("Arial", 12), placeholder_text="Username", fg_color="white", text_color="black", placeholder_text_color="grey")
        self.Username_entry.grid(row=1, column=1)

        self.Password_label = ctk.CTkLabel(self.main_frame, text="Password:", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Password_label.grid(row=2, column=0, sticky="e")

        self.Password_entry = ctk.CTkEntry(self.main_frame, width=250, font=("Arial", 12), show="*", placeholder_text="Password", fg_color="white", text_color="black", placeholder_text_color="grey")
        self.Password_entry.grid(row=2, column=1)

        self.Login_button = ctk.CTkButton(self.main_frame, text="Login", fg_color="#1c1c1c", text_color="white", hover_color="#282828", border_width=1, border_color="#424242", font=("Arial", 14, "bold"), command=self.Login)
        self.Login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.error_label = ctk.CTkLabel(self.main_frame, text="", text_color="red", fg_color="#1c1c1c", font=("Arial", 14, "bold"))
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(10,0))

        bottom_frame = ctk.CTkFrame(self.main_frame, fg_color=self.main_frame.cget("fg_color"))
        bottom_frame.grid(row=5, column=0, columnspan=2, pady=20)

        self.not_signed_label = ctk.CTkLabel(bottom_frame, text="Don't have an account?", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.not_signed_label.grid(row=0, column=0)

        self.signup_link = ctk.CTkLabel(bottom_frame, text="Sign up.", font=("Arial",13, "bold", "underline"), text_color="#001eff", fg_color="#1c1c1c", cursor="hand2")
        self.signup_link.grid(row=0, column=1, padx=0)

        self.signup_link.bind("<Button-1>", self.on_signup_click)

        self.root.mainloop()

    def Login(self):
        Username = self.Username_entry.get()
        Password = self.Password_entry.get()
        self.error_label.configure(text="")
        if Username == "" or Password == "":
            self.error_label.configure(text="Fill in all fields")
        elif (len(Username) < 3) or (len(Username) > 30):
            self.error_label.configure(text="Username is too short")
        elif (len(Password) < 8) or (len(Password) > 16):
            self.error_label.configure(text="Password length invalid! (8-16)")
        else:
            if self.Validate_password(Password):
                self.error_label.configure(text="Login Successful")

    def Validate_password(self, password):
        Validity = [False, False, False, False]
        for char in password:
            if char.isalpha() and (char == char.upper()): # Checks for uppercase letters
                Validity[0] = True
            if char.isalpha() and (char == char.lower()): # Checks for lowercase letters
                Validity[1] = True
            if char.isdigit(): # Checks for numbers
                Validity[2] = True
            if (not char.isalpha()) and (not char.isdigit()): # Checks for symbols
                Validity[3] = True

        if not Validity[0]:
            self.error_label.configure(text="Password must contain at least 1 uppercase letter!")
            return False
        elif not Validity[1]:
            self.error_label.configure(text="Password must contain at lest 1 lowercase letter!")
            return False
        elif not Validity[2]:
            self.error_label.configure(text="Password must contain at least 1 number!")
            return False
        elif not Validity[3]:
            self.error_label.configure(text="Password must contain at least 1 symbol!")
            return False
        else:
            return True

    def on_signup_click(self, event):
        pass

Login_GUI()