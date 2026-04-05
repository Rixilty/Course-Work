import customtkinter as ctk
import locale
import threading
import asyncio
from googletrans import Translator, LANGUAGES

# Initializing the translator
translator = Translator()

class LanguageManager:
    def __init__(self):
        # Detecting the system language automatically
        try:
            # Gets something like "en_GB" or "fr_FR", so we need to take the first 2 characters, as that's the code that googletrans recognises
            sys_code = locale.getlocale()[0][:2]
        except:
            # In case of an error we just set it to english
            sys_code = "en"

        self.code = "en" # Initializing self.code

        if sys_code in LANGUAGES:
            # If the language code we extracted exists in LANGUAGES, which is the list of code googltrans uses then we set it to self.code
            self.code = sys_code

        # Set the initial name based on the detected code
        self.name = LANGUAGES[self.code].title()

    def get_all_languages(self):
        # This returns a storted list of languages names for the dropdown menu
        languages_list = []
        for lang in LANGUAGES.values():
            lang_name = lang.title()
            languages_list.append(lang_name)

        languages_list.sort()
        return languages_list

    def get_code(self, name):
        # Reverse lookup e.g. "spanish" --> "es"
        for code, lang_name in LANGUAGES.items():
            if lang_name.lower() == name.lower():
                return code
            return "en"

# Creating a global variable to track user's choice
lang_data = LanguageManager()

class LanguageSplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Language Selection")
        self.geometry("550x450")
        self.configure(fg_color="#1c1c1c")

        # GUI

        # Header
        ctk.CTkLabel(self, text="Language Detection", font=("Arial", 29, "bold")).pack(pady=(40,10))

        self.info_label = ctk.CTkLabel(self, text=f"We detected your language as: {lang_data.name}", font=("Arial", 20, "bold"))
        self.info_label.pack(pady=10)

        # Dropdown Selection
        ctk.CTkLabel(self, text="Not your preferred language?", text_color="grey").pack(pady=20)
        self.lang_dropdown = ctk.CTkOptionMenu(self, values=lang_data.get_all_languages(), command=self.manual_change, width=200)
        self.lang_dropdown.set(lang_data.name)
        self.lang_dropdown.pack(pady=10)

        # Seperator
        ctk.CTkLabel(self, text="--- OR ---", text_color="grey").pack(pady=10)

        # Detect a language through a phrase instead
        self.phrase_entry = ctk.CTkEntry(self, placeholder_text="Type a phrase in your language...", width=300)
        self.phrase_entry.pack(pady=5)

        self.detect_button = ctk.CTkButton(self, text="Detect from phrase", command=self.start_detection_thread)
        self.detect_button.pack(pady=5)

        # Confirmation button
        self.confirm_button = ctk.CTkButton(self, text="Confirm & Continue", height=40, command=self.finish_setup)
        self.confirm_button.pack(side="bottom", pady=20)

    # Procedures and Functions

    def manual_change(self, choice):
        lang_data.name = choice
        lang_data.code = lang_data.get_code(choice)
        self.info_label.configure(text=f"Language set to: {choice}")

    def start_detection_thread(self):
        # Detection is ran in a thread so the UI doesn't freeze
        phrase = self.phrase_entry.get()
        if not phrase:
            return

        self.detect_button.configure(state="disabled", text="Detecting...")
        threading.Thread(target=self.detect_logic, args=(phrase,), daemon=True).start()

    def detect_logic(self, text):
        # Googletrans is async so it's handled here
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(translator.detect(text))

            # Getting the name from the code
            detected_name = LANGUAGES[result.lang].title()

            # Updating the UI safely back on the main thread
            self.after(0, lambda: self.update_ui_after_detect(detected_name))
        except Exception as e:
            self.after(0, lambda: self.detect_button.configure(state="normal", text="Detection failed!"))

    def update_ui_after_detect(self, name):
        self.lang_dropdown.set(name)
        self.manual_change(name)
        self.detect_button.configure(state="normal", text="Detect from phrase")
        self.info_label.configure(text=f"Detected: {name}")

    def finish_setup(self):
        print(lang_data.name, lang_data.code)
        # call the Login screen
        # self.destroy()
        # LoginWindow().mainloop()
        self.confirm_button.configure(state="disabled", text="Setting up...")

if __name__ == "__main__":
    app = LanguageSplashScreen()
    app.mainloop()