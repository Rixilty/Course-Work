import customtkinter as ctk
import socket

class ParentGUI:

    def close_window(self):
        # Safely close the window

        if self.root:
            for after_id in self.root.tk.eval("after info").split():
                self.root.after_cancel(after_id)
            self.root.destroy()

    # This is the base class from which the signup and login GUI will inherit from

    def __init__(self, title="title"):
        self.root = None
        self.main_frame = None
        self.title_text = title
        self.window_width = 550
        self.window_height = 420

    def window(self):
        # This procedure sets up the configurations of the main window: position, geometry, colours etc.
        self.root = ctk.CTk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - self.window_width) / 2)
        y = int((screen_height - self.window_height) / 2)

        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.title(self.title_text)
        self.root.configure(fg_color="#1c1c1c")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def frames(self):
        # This procedure creates the frames for the GUI
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1c1c1c")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0) # Top frame
        self.main_frame.rowconfigure(1, weight=1) # Content frame
        self.main_frame.rowconfigure(2, weight=0) # Bottom frame

        # Top frame for the title
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c")  # Fixed frame
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 5))
        self.top_frame.grid_columnconfigure(0, weight=1)

        # Content frame for main contents of the GUI
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c")
        self.content_frame.grid(row=1, column=0, sticky="")
        self.content_frame.grid_columnconfigure(0, weight=0)
        self.content_frame.grid_columnconfigure(1, weight=0)

        # Bottom frame for buttons and links
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="#1c1c1c")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=0)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

    def create_title(self, title_text):
        # This procedure creates the title label
        self.Title = ctk.CTkLabel(self.top_frame, text=title_text, font=("Arial", 31, "bold"), text_color="white",fg_color="#1c1c1c")
        self.Title.grid(row=0, column=0, columnspan=2, sticky="n", pady=10)

    def create_username_field(self):
        # This procedure creates a username field with validation

        # Username label
        self.Username_label = ctk.CTkLabel(self.content_frame, text="Username:", font=("Arial", 13, "bold"),text_color="white", fg_color="#1c1c1c")
        self.Username_label.grid(row=1, column=0, sticky="e", padx=(0, 10))

        # Username entry
        self.Username_entry = ctk.CTkEntry(self.content_frame, width=250, font=("Arial", 12),placeholder_text="Username", fg_color="white", text_color="black",placeholder_text_color="grey")
        self.Username_entry.grid(row=1, column=1, pady=5)

        # Username requirements frame (hidden by default)
        self.username_requirements_frame = ctk.CTkFrame(self.content_frame, fg_color="#1c1c1c")
        self.username_requirements_frame.grid(row=2, column=1, sticky="w", pady=(5, 0))
        self.username_length_requirement = ctk.CTkLabel(self.username_requirements_frame,text="● Username Length Must Be Between 3-16", text_color="red")

        # Pack username requirement
        self.username_length_requirement.pack(anchor="w")

        # Making it not visible by default
        self.username_requirements_frame.grid_remove()

        # Bind events for the username field
        self.Username_entry.bind("<FocusIn>", lambda e: self.username_requirements_frame.grid())
        self.Username_entry.bind("<FocusOut>", lambda e: self.username_requirements_frame.grid_remove())
        self.Username_entry.bind("<KeyRelease>", self.check_username_requirements)

    def create_password_field(self):
        # This procedure creates a password field with validation

        # Password label
        self.Password_label = ctk.CTkLabel(self.content_frame, text="Password:", font=("Arial", 13, "bold"),text_color="white", fg_color="#1c1c1c")
        self.Password_label.grid(row=3, column=0, sticky="e", padx=(0, 10))

        # Password entry
        self.Password_entry = ctk.CTkEntry(self.content_frame, width=250, font=("Arial", 12), show="*",placeholder_text="Password", fg_color="white", text_color="black",placeholder_text_color="grey")
        self.Password_entry.grid(row=3, column=1, pady=5)

        # Password requirements frame (hidden by default)
        self.password_requirements_frame = ctk.CTkFrame(self.content_frame, fg_color="#1c1c1c")
        self.password_requirements_frame.grid(row=4, column=1, sticky="w", pady=(5, 0))

        # Password requirements labels
        self.uppercase_requirement = ctk.CTkLabel(self.password_requirements_frame,text="● At least 1 Uppercase Letter", text_color="red")
        self.lowercase_requirement = ctk.CTkLabel(self.password_requirements_frame,text="● At least 1 Lowercase Letter", text_color="red")
        self.digit_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Number",text_color="red")
        self.symbol_requirement = ctk.CTkLabel(self.password_requirements_frame, text="● At least 1 Symbol",text_color="red")
        self.password_length_requirement = ctk.CTkLabel(self.password_requirements_frame,text="● Password Length Must Be Between 8-16", text_color="red")

        # Pack all password requirement labels
        self.uppercase_requirement.pack(anchor="w")
        self.lowercase_requirement.pack(anchor="w")
        self.digit_requirement.pack(anchor="w")
        self.symbol_requirement.pack(anchor="w")
        self.password_length_requirement.pack(anchor="w")

        # Making it not visible by default
        self.password_requirements_frame.grid_remove()

        # Bind events for password field
        self.Password_entry.bind("<FocusIn>", lambda e: self.password_requirements_frame.grid())
        self.Password_entry.bind("<FocusOut>", lambda e: self.password_requirements_frame.grid_remove())
        self.Password_entry.bind("<KeyRelease>", self.check_password_requirements)

    def create_error_label(self):
        # This procedure creates error/success message labels

        # Error label
        self.error_label = ctk.CTkLabel(self.main_frame, text="", text_color="red", fg_color="#1c1c1c",font=("Arial", 14, "bold"))
        self.error_label.grid(row=6, column=0, columnspan=2, pady=(10, 0))

    def create_button(self, text, command):
        # This procedure creates the Login/Signup button
        self.Login_button = ctk.CTkButton(self.bottom_frame, text=text, fg_color="#1c1c1c", text_color="white",hover_color="#282828", border_width=1, border_color="#424242",font=("Arial", 14, "bold"), command=command)
        self.Login_button.grid(row=5, column=0, columnspan=2, sticky="n", pady=(10, 0))

    def create_link(self, prompt_text, link_text, command):
        # This procedure creates links to switch between Login and Signup

        # Prompt label
        self.prompt_label = ctk.CTkLabel(self.bottom_frame, text=prompt_text,font=("Arial", 13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.prompt_label.grid(row=0, column=0, sticky="e")

        # Link label
        self.link = ctk.CTkLabel(self.bottom_frame, text=link_text, font=("Arial", 13, "bold", "underline"),text_color="#001eff", fg_color="#1c1c1c", cursor="hand2")
        self.link.grid(row=0, column=1, padx=0, sticky="w")
        self.link.bind("<Button-1>", command)

    def check_username_requirements(self, event=None):
        # This procedure checks if the username entered by the user meets the length requirement

        # Get the username entered by the user
        Username = self.Username_entry.get()

        # Sets the label colour to red indicating the requirement not met
        self.username_length_requirement.configure(text_color="red")

        # If the requirement is met the label colour is set to green
        if len(Username) > 2 and len(Username) < 16:
            self.username_length_requirement.configure(text_color="green")

    def check_password_requirements(self, event=None):
        # This procedure checks if the password entered by the user meets all the requirements

        # Get the passoword entered by the user
        Password = self.Password_entry.get()

        # Loops through every label and sets their colour to red
        for i in [self.password_length_requirement, self.uppercase_requirement, self.lowercase_requirement, self.digit_requirement, self.symbol_requirement]:
            i.configure(text_color="red")

        # Checks if the password length is valid if so set the label colour to green
        if len(Password) > 8 and len(Password) < 16:
            self.password_length_requirement.configure(text_color="green")

        # Loops through every character in the password and checks if a unique character from each set is used if so, the corresponding label colour is set to green
        for i in Password:
            if i.isupper():  # Checks for uppercase letters
                self.uppercase_requirement.configure(text_color="green")
            if i.islower():  # Checks for lowercase letters
                self.lowercase_requirement.configure(text_color="green")
            if i.isdigit():  # Checks for numbers
                self.digit_requirement.configure(text_color="green")
            if not i.isalnum():  # Checks for symbols
                self.symbol_requirement.configure(text_color="green")

    def validate_fields(self):

        # This function validates all input fields and returns True/False and an error message

        Username = self.Username_entry.get()
        Password = self.Password_entry.get()

        if Username == "" or Password == "":
            return False, "Fill in all fields!"

        if self.username_length_requirement.cget("text_color") == "red":
            return False, "Username must be 3-16 characters!"

        if self.uppercase_requirement.cget("text_color") == "red":
            return False, "Password must contain at least one uppercase letter!"

        if self.lowercase_requirement.cget("text_color") == "red":
            return False, "Password must contain at least one lowercase letter!"

        if self.digit_requirement.cget("text_color") == "red":
            return False, "Password must contain at least one number!"

        if self.symbol_requirement.cget("text_color") == "red":
            return False, "Password must contain at least one symbol!"

        if self.password_length_requirement.cget("text_color") == "red":
            return False, "Password must be 8-16 characters!"

        return True, "Login Successful!"

class LoginGUI(ParentGUI):
    # This is the Login GUI class which inherits from the Parent GUI class

    def __init__(self):
        super().__init__(title="Login")
        self.auth = Authentication # Creates the client
        self.window()
        self.frames()
        self.create_title("Login")
        self.create_username_field()
        self.create_password_field()
        self.create_error_label()
        self.create_button("Login", self.login)
        self.create_link("Don't have an account?", "Sign up.", self.on_signup_clicked)
        self.root.mainloop()

    def login(self):
        # This runs when the login button is clicked

        # Get credentials from the input fields
        username = self.Username_entry.get()
        password = self.Password_entry.get()

        # This checks if the credentials entered are valid and returns a message (this runs locally)
        is_valid, message = self.validate_fields()

        # If the credentials aren't valid we return an error message
        if not is_valid:
            self.error_label.configure(text=message, text_color="red")
            return

        # Show "Logging in..." message
        self.error_label.configure(text="Logging in...", text_color="white")

        self.root.update() # This forces the GUI to update to show the message

        # Send to server
        print("Sending credentials...")
        response = self.auth.send_login(username, password)

        # Handle server respons
        if response["status"] == "success":
            self.error_label.configure(text="Login Successful!", text_color="green")
            # Open main application window
        else:
            self.error_label.configure(text="Login Failed!", text_color="red")

    def on_signup_clicked(self, event):
        # This runs when the signup link is clicked and switches the GUI
        # Closes the current window
        self.close_window()
        #open signup window
        signup_gui = SignupGUI()

class SignupGUI(ParentGUI):
    # This is the Signup GUI class which inherits from the Parent GUI class}

    def __init__(self):
        super().__init__(title="Sign up")
        self.auth = Authentication() # This creates the client
        self.window_height = 450 # Slightly taller for confirm password field
        self.window()
        self.frames()
        self.create_title("Sign Up")
        self.create_username_field()
        self.create_password_field()
        self.create_confirm_password_field()
        self.create_error_label()
        self.create_button("Sign Up", self.signup)
        self.create_link("Already have an account?", "Login.", self.on_login_clicked)
        self.root.mainloop()

    def create_confirm_password_field(self):
        # This procedure creates a new confirm password field which is specific to the signup GUI

        # Confirm password label
        self.Confirm_password_label = ctk.CTkLabel(self.content_frame, text="Password:", font=("Arial",13, "bold"), text_color="white", fg_color="#1c1c1c")
        self.Confirm_password_label.grid(row=5, column=0, sticky="e", padx=(0,10))

        # Confirm password entry
        self.Confirm_password_entry = ctk.CTkEntry(self.content_frame, width=250, font=("Arial", 12), show="*",placeholder_text="Password", fg_color="white", text_color="black",placeholder_text_color="grey")
        self.Confirm_password_entry.grid(row=5, column=1, pady=5)

        # Password match requirement
        self.password_match_frame = ctk.CTkFrame(self.content_frame, fg_color="#1c1c1c")
        self.password_match_frame.grid(row=6, column=1, sticky="w", padx=(5,0))

        self.password_match_requirement = ctk.CTkLabel(self.password_match_frame, text="● Passwords must match", text_color="red")
        self.password_match_requirement.pack(anchor="w")

        # Bind event to check that the passwords match
        self.Confirm_password_entry.bind("<KeyRelease>", self.check_password_match)

    def check_password_match(self, event=None):
        # This procedure checks if the passwords match

        password = self.Password_entry.get()
        confirm_password = self.Confirm_password_entry.get()

        # This checks if the passwords are the same and that password is not empty as that will trigger it to be true
        if (confirm_password == password) and password !="":
            self.password_match_requirement.configure(text_color="green")
        else:
            self.password_match_requirement.configure(text_color="red")

    def validate_fields(self):
        # Overriding to add confirm password validation

        is_valid, message = super().validate_fields()

        if not is_valid:
            return False, message

        # Check if passwords match
        password = self.Password_entry.get()
        confirm_password = self.Confirm_password_entry.get()

        if password != confirm_password:
            return False, "Passwords do not match!"

        return True, ""

    def signup(self):
        # This runs when the signup button is clicked

        # Get credentials
        username = self.Username_entry.get()
        password = self.Password_entry.get()
        confirm_password = self.Confirm_password_entry.get()

        # Validate locally
        is_valid, message = self.validate_fields()

        if not is_valid:
            self.error_label.configure(text=message, text_color="red")
            return

        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match!", text_color="red")
            return

        # Show "Creating account..." message
        self.error_label.configure(text="Creating account...", text_color="white")
        self.root.update()

        # Send to server
        print("Sending credentials...")
        response = self.auth.send_signup(username, password)

        # Handle server response
        if response["status"] == "success":
            self.error_label.configure(text="Sign up Successful!", text_color="green")
            self.root.after(2000, self.on_login_clicked)
        else:
            self.error_label.configure(text=["message"], text_color="red")

    def on_login_clicked(self, event):
        # This runs when the login link is clicked and switches the GUI
        # Closes the current window
        self.close_window()

        # open login window
        login_gui = LoginGUI()

class Authentication:
    # This handles communication with the authentication server

    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port

    def send_login(self, username, password):
        # This sends login request to the server
        return self.send_request("/l", username, password) # /l is read by the server and interpreted as a login request

    def send_signup(self, username, password):
        # This sends signup requests to server
        return self.send_request("/s", username, password)

    def send_request(self, command, username, password):
        # This sends requests in the format /command:username:password
        try:
            # Create a socket connection
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5) # 5 second timeout
            client_socket.connect((self.host, self.port))

            # Format the request --> /command:username:password
            request = f"{command}:{username}:{password}"
            print(f"Sending {request} to server...") # Here for debugging

            # Send the request
            client_socket.send(request.encode("utf-8"))

            #Receive response
            response = client_socket.recv(1024).decode("utf-8")
            client_socket.close()

            print(f"Server response: {response}")
            return self.parse_response(response)

        except socket.timeout:
            return {"status": "error", "message": "Connection timed out - server not responding"}
        except ConnectionRefusedError:
            return {"status": "error", "message": "Cannot connect to server"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def parse_response(self, response):
        # Parse server response: SUCCESS: message or ERROR: message
        response = response.strip()

        if response.startswith("SUCCESS:"):
            return {"status": "success", "message": response[8:].strip()} # Removes SUCCESS: from the message
        elif response.startswith("ERROR:"):
            return {"status": "error", "message": response[8:].strip()} # Removes ERROR: from the message
        else:
            return {"status": "error", "message": f"Unexcpected error: {response}"}

# Start the GUI
if __name__ == "__main__":
    login_gui = LoginGUI()