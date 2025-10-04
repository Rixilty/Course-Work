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
        self.Login_button = tk.Button(self.root, text="Login")
        self.Login_button.pack()

        self.root.mainloop()

Login_GUI()