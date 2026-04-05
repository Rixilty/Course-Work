import os
from Client.LanguageSelection import LanguageSplashScreen
from Client.Updated_GUI import LoginGUI

CONFIG_FILE = "config.txt"

def language_already_selected():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            content = f.read().strip().lower() # Reading the text
            if content == "null" or content == "":
                return False
            return content

def main():
    language = language_already_selected()
    if not language:
        print("First launch detected. Opening splash program")
        app = LanguageSplashScreen()
        app.mainloop()
    else:
        print(f"User preferred language is {language}. Opening Login program")
        app = LoginGUI()
        app.mainloop()

if __name__ == "__main__":
    main()
