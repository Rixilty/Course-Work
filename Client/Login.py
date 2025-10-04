import tkinter as tk
from tkinter import messagebox

class Login_GUI:

    def __init__(self):

        self.root = tk.Tk()

        self.root.geometry("400x300")
        self.root.title("Login")

        self.Title = tk.Label(self.root, text="Login")
        self.Title.pack()
        self.Username_entry = tk.Entry(self.root, text="Username")
        self.Username_entry.pack()
        self.Password_entry = tk.Entry(self.root, text="Password")
        self.Password_entry.pack()
        self.Login_button = tk.Button(self.root, text="Login", command=self.Login)
        self.Login_button.pack()

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
            self.Validate_password(Password)
            if self.Validate_password(Password):
                messagebox.showinfo("Success", "Login Successful")

    def Validate_password(self, password):
        Validity = [False, False, False, False]
        for char in password:
            if char == char.upper(): # Checks for uppercase letters
                Validity[0] = True
            if char == char.lower(): # Checks for lowercase letters
                Validity[1] = True
            if char.isdigit(): # Checks for numbers
                Validity[2] = True
            if (char != char.ischar()) and (char != char.isdigit()): # Checks for symbols
                Validity[3] = True

        if not Validity[0]:
            return messagebox.showerror("Error", "Password must contain at least 1 uppercase letter!")
        elif not Validity[1]:
            return messagebox.showerror("Error", "Password must contain at lest 1 lowercase letter!")
        elif not Validity[2]:
            return messagebox.showerror("Error", "Password must contain at least 1 number!")
        elif not Validity[3]:
            return messagebox.showerror("Error", "Password must contain at least 1 symbol!")
        else:
            return True


Login_GUI()