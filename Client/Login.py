import tkinter as tk
from tkinter import messagebox


class Login_GUI:

    def __init__(self):

        window_width = 500
        window_height = 350

        self.root = tk.Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.title("Login")
        self.root.configure(bg="#1c1c1c")

        self.main_frame = tk.Frame(self.root, bg="#1c1c1c")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.Title = tk.Label(self.main_frame, text="Login", font=("Arial", 31, "bold"), fg="white", bg="#1c1c1c")
        self.Title.grid(row=0, column=0, columnspan=2, pady=20)

        self.Username_label = tk.Label(self.main_frame, text="Username:", font=("Arial",13, "bold"), fg="white", bg="#1c1c1c")
        self.Username_label.grid(row=1, column=0, sticky="e")

        self.Username_entry = tk.Entry(self.main_frame, width=31, font=("Arial", 12))
        self.Username_entry.grid(row=1, column=1)
        self.add_placeholder(self.Username_entry, "Username")

        self.Password_label = tk.Label(self.main_frame, text="Password:", font=("Arial",13, "bold"), fg="white", bg="#1c1c1c")
        self.Password_label.grid(row=2, column=0, sticky="e")

        self.Password_entry = tk.Entry(self.main_frame, width=31, font=("Arial", 12), show="*")
        self.Password_entry.grid(row=2, column=1)
        self.add_placeholder(self.Password_entry, "Password", is_password=True)


        button_border = tk.Frame(self.main_frame, bg="#424242")
        button_border.grid(row=3, column=0, columnspan=2, pady=10)
        self.Login_button = tk.Button(button_border, text="Login", bg="#1c1c1c", fg="white", activebackground="#282828", activeforeground="white", borderwidth=0, font=("Arial", 14, "bold"), command=self.Login)
        self.Login_button.grid(row=0, column=0, padx=1, pady=1)

        self.error_label = tk.Label(self.main_frame, text="", fg="red", bg="#1c1c1c", font=("Arial", 14, "bold"))
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(10,0))

        bottom_frame = tk.Frame(self.main_frame, bg=self.main_frame["bg"])
        bottom_frame.grid(row=4, column=0, columnspan=2, pady=20)

        self.not_signed_label = tk.Label(bottom_frame, text="Don't have an account?", font=("Arial",13, "bold"), fg="white", bg="#1c1c1c")
        self.not_signed_label.grid(row=0, column=0)

        self.signup_link = tk.Label(bottom_frame, text="Sign up.", font=("Arial",13, "bold underline"), fg="#001eff", bg="#1c1c1c", cursor="hand2")
        self.signup_link.grid(row=0, column=1, padx=0)

        self.signup_link.bind("<Button-1>", self.on_signup_click)

        self.root.mainloop()

    def Login(self):
        Username = self.Username_entry.get()
        Password = self.Password_entry.get()
        self.error_label.config(text="")
        if (Username == "") or (Password == ""):
            self.error_label.config(text="Fill in all fields")
        elif (len(Username) < 3):
            self.error_label.config(text="Username is too short")
        elif (len(Password) < 8) or (len(Password) > 16):
            self.error_label.config(text="Password length invalid! (8-16)")
        else:
            if self.Validate_password(Password):
                self.error_label.config(text="Login Successful")

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
            self.error_label.config(text="Password must contain at least 1 uppercase letter!")
            return False
        elif not Validity[1]:
            self.error_label.config(text="Password must contain at lest 1 lowercase letter!")
            return False
        elif not Validity[2]:
            self.error_label.config(text="Password must contain at least 1 number!")
            return False
        elif not Validity[3]:
            self.error_label.config(text="Password must contain at least 1 symbol!")
            return False
        else:
            return True

    def add_placeholder(self, entry, placeholder_text, is_password=False):
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")
        if is_password:
            entry.config(show="")

        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")
                entry.config(fg="black")
                if is_password:
                    entry.config(show="*")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder_text)
                entry.config(fg="grey")
                if is_password:
                    entry.config(show="")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def on_signup_click(self, event):
        pass

Login_GUI()