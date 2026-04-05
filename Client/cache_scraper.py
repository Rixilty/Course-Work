import os
import json
import Translator
from googletrans import LANGUAGES

#importing my class
from LanguageSelection import LanguageSplashScreen
from Main import MessagingApp
from Updated_GUI import ParentGUI
from Updated_GUI import LoginGUI
from Updated_GUI import SignupGUI

def generate_json_files():
    # Find all the English strings first
    print("Finding strings...")
    discovered_strings = set()

    # Temporarily point config to English so we can get the base strings
    with open("config.txt", "w") as f:
        f.write("en")

    original_translate = Translator.translate_text
    Translator.translate_text = lambda text: (discovered_strings.add(text), text)[1]

    # Initializing the apps this triggers the __init__ and translate_text calls
    LanguageSplashScreen()
    MessagingApp("ScarpingBot")
    ParentGUI()
    LoginGUI()
    SignupGUI()

    # Restoring the original function for the actual translation loop
    Translator.translate_text = original_translate
    print(f"Found {len(discovered_strings)} strings to translate.")

    # Looping through every language and rewrite config.txt
    os.makedirs("languages", exist_ok=True)

    for code in LANGUAGES.keys():
        print(f"Processing: {code} ({LANGUAGES[code]})")

        # Change the code in the config file for each iteration
        with open("config.txt", "w") as f:
            f.write(code)

        cache = {}
        for i in discovered_strings:
            # This reads the code from config.txt and calls the API
            cache[i] = Translator.translate_text(i)

        # Save into a json file
        with open(f"languages/{code}.json", "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    os.environ["SCRAPING"] = "true"
    generate_json_files()