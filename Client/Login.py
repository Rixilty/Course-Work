import tkinter as tk
from tkinter import messagebox

class Login_GUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.geometry("400x300")
        self.root.title("Login")

        self.Title = tk.Label(self.root, text="Login", font=("Arial", 16))
        self.Title.grid(row=0, column=0, columnspan=2, pady=20)

        self.Username_label = tk.Label(self.root, text="Username:")
        self.Username_label.grid(row=1, column=0, sticky="e", padx=10)

        self.Username_entry = tk.Entry(self.root, width=25)
        self.Username_entry.grid(row=1, column=1, padx=10)
        self.add_placeholder(self.Username_entry, "Username")

        self.Password_label = tk.Label(self.root, text="Password:")
        self.Password_label.grid(row=2, column=0, sticky="e", padx=10)

        self.Password_entry = tk.Entry(self.root, width=25, show="*")
        self.Password_entry.grid(row=2, column=1, padx=10)
        self.add_placeholder(self.Password_entry, "Password")

        self.Login_button = tk.Button(self.root, text="Login", command=self.Login)
        self.Login_button.grid(row=3, column=0, columnspan=2, padx=15)

        self.root.mainloop()

    def Login(self):
        Username = self.Username_entry.get()
        Password = self.Password_entry.get()
        if (Username == "") or (Password == ""):
            messagebox.showerror("Error", "Fill in all fields")
        elif (len(Username) < 3):
            messagebox.showerror("Error", "Username is too short")
        elif (len(Password) < 8) or (len(Password) > 16):
            messagebox.showerror("Error", "Password length invalid! (8-16)")
        else:
            if self.Validate_password(Password):
                messagebox.showinfo("Success", "Login Successful")

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
            messagebox.showerror("Error", "Password must contain at least 1 uppercase letter!")
            return False
        elif not Validity[1]:
            messagebox.showerror("Error", "Password must contain at lest 1 lowercase letter!")
            return False
        elif not Validity[2]:
            messagebox.showerror("Error", "Password must contain at least 1 number!")
            return False
        elif not Validity[3]:
            messagebox.showerror("Error", "Password must contain at least 1 symbol!")
            return False
        else:
            return True

    def add_placeholder(self, entry, placeholder_text):
        entry.insert(0, placeholder_text)
        entry.config(fg="grey")

        def on_focus_in(event):
            if event.get() == placeholder_text:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if event.get() == "":
                entry.insert(0, placeholder_text)
                entry.config(fg="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

Login_GUI()